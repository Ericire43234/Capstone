import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import os
from scipy.signal import find_peaks
from scipy.stats import linregress

# Get the directory containing the CSV files
csv_dir = Path(__file__).parent / 'CNC_Nylon_Tests_2_(80k)_3k'

# Find all CSV files in the directory
csv_files = sorted(csv_dir.glob('*.csv'))

# Create a figure
fig = go.Figure()

# Color palette for different cycles
colors = [
    '#1f77b4',  # blue
    '#ff7f0e',  # orange
    '#2ca02c',  # green
    '#d62728',  # red
    '#9467bd',  # purple
    '#8c564b',  # brown
]

# Collect max forces for each test
all_max_forces = []
prev_cycles = [0]
unique_cycles = []
for idx, csv_file in enumerate(csv_files):
    df = pd.read_csv(csv_file, skiprows=8)  # Skip metadata and header rows
    
    # Rename columns to be the actual names
    df.columns = ['CycleCount', 'Time', 'AxialCount', 'Displacement', 'Force']
    
    # Convert to numeric (remove any quotes)
    df['CycleCount'] = pd.to_numeric(df['CycleCount'], errors='coerce')
    df['Time'] = pd.to_numeric(df['Time'], errors='coerce')
    df['Displacement'] = pd.to_numeric(df['Displacement'], errors='coerce')
    df['Force'] = pd.to_numeric(df['Force'], errors='coerce')

    # Smooth force before extracting per-cycle extrema
    # min_periods=1 avoids NaN values at the edges when center=True
    df['ForceSmoothed'] = (
        df['Force']
        .rolling(window=10, center=True, min_periods=1)
        .mean()
    )

    # Count internal cycles and get max force per cycle from smoothed force
    cycle_max = df.groupby('CycleCount')['ForceSmoothed'].max().values
    cycle_min = df.groupby('CycleCount')['ForceSmoothed'].min().values
    max_forces = cycle_max - cycle_min  # Calculate force range for each cycle
    #num_cycles = len(max_forces)
    unique_cycles.append(sorted(df['CycleCount'].unique()))

    #print(f"last {unique_cycles[-1]}")
    #print(f"File: {csv_file.name}, Number of cycles: {num_cycles}, Unique cycles: {unique_cycles}")
    
    # Filter out forces below 1 lbf
    #max_forces = max_forces[max_forces <= 2.8]
    
    #print("Length of max forces after filtering:", len(max_forces))
    all_max_forces.append(max_forces)
    prev_cycles.append(unique_cycles[-1][-1])  # Update cumulative cycle count


# Create a figure for max force vs cycle number
fig = go.Figure()

all_cycles = []
all_forces = []

for idx, forces in enumerate(all_max_forces):
    cycles = [cycle+prev_cycles[idx] for cycle in unique_cycles[idx]]
    all_cycles.extend(cycles)
    all_forces.extend(forces)
    fig.add_trace(go.Scatter(
        x=cycles,
        y=forces,
        mode='lines+markers',
        name=f'Test {idx + 1}',
        line=dict(
            color=colors[idx % len(colors)],
            width=2
        ),
        hovertemplate='<b>Test %{fullData.name}</b><br>Cycle: %{x}<br>Max Force: %{y:.4f} lbf<extra></extra>'
    ))
    

# Add linear fit across all data
try:
    slope, intercept, r, p, se = linregress(all_cycles, all_forces)
    fit_line = [slope * x + intercept for x in all_cycles]
    fig.add_trace(go.Scatter(
        x=all_cycles,
        y=fit_line,
        mode='lines',
        name='Linear Fit',
        line=dict(color='black', dash='dash', width=3),
        hovertemplate='Linear Fit: %{y:.4f} lbf<extra></extra>'
    ))
except Exception as e:
    print(f"Error performing linear regression: {e}")
    slope, intercept, r = 0, 0, 0  # Default values if fit fails

# Calculate estimated force at 100,000 cycles
est_100k = slope * 100000 + intercept
drop = intercept - est_100k

# Add annotation with fit info
fit_text = f"Slope (per 10k cycles): {slope * 10000:.6f}<br>Intercept: {intercept:.6f}<br>R²: {r**2:.4f}<br>Force at 100k cycles: {est_100k:.2f} lbf<br>Estimated Total drop (0 to 100k): {drop:.2f} lbf"
fig.add_annotation(
    text=fit_text,
    xref="paper", yref="paper",
    x=0.98, y=0.8,
    xanchor="right",
    yanchor="top",
    showarrow=False,
    font=dict(size=12),
    align="left",
    bgcolor="white",
    bordercolor="black",
    borderwidth=1
)

#print(f"Linear fit: slope (per 10k cycles) = {slope * 10000:.6f}, intercept = {intercept:.6f}, r^2 = {r**2:.4f}")
#print(f"Estimated force at 100,000 cycles: {est_100k:.2f} lbf")
#print(f"Total estimated drop in force (0 to 100k cycles): {drop:.2f} lbf")
force_at_100k = slope * 100000 + intercept
#print(f"Predicted max force at 100,000 cycles: {force_at_100k} lbf")

csv_file_names = ', '.join([csv_file.name for csv_file in csv_files])

# Update layout
fig.update_layout(
    title=f'Max Force vs Cycle Number Across Tests<br><sup>{csv_file_names}</sup>',
    xaxis_title='Cycle Number',
    yaxis_title='Max Force (lbf)',
    hovermode='x unified',
    width=1200,
    height=700,
    template='plotly_white',
    legend=dict(
        yanchor='top',
        y=0.99,
        xanchor='right',
        x=0.99
    )
)

# Show the plot
fig.show()

# Optionally save the plot
output_file = Path(__file__).parent / 'Max_Force_vs_Cycles_Interactive.html'
fig.write_html(str(output_file))
print(f"Interactive plot saved to: {output_file}")
