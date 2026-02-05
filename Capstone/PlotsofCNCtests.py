import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import os
from scipy.signal import find_peaks
from scipy.stats import linregress

# Get the directory containing the CSV files
csv_dir = Path(__file__).parent / 'CNC_Delrin_Tests'

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
prev_cycles = 0  # To keep track of cumulative cycles across tests
for idx, csv_file in enumerate(csv_files):
    df = pd.read_csv(csv_file, skiprows=2)  # Skip header and units row
    
    # Rename columns to be the actual names
    df.columns = ['Time', 'Displacement', 'Force']
    
    # Convert to numeric (remove any quotes)
    df['Time'] = pd.to_numeric(df['Time'], errors='coerce')
    df['Displacement'] = pd.to_numeric(df['Displacement'], errors='coerce')
    df['Force'] = pd.to_numeric(df['Force'], errors='coerce')
    
    # Count internal cycles based on force peaks
    diff = df['Force'].diff()
    peaks = (diff > 0) & (diff.shift(-1) < 0)
    num_cycles = peaks.sum()
    #print(f"{csv_file.name}: {num_cycles} internal cycles")
    
    # Extract max force at each peak
    max_forces = df.loc[peaks, 'Force'].values
    
    # Filter out forces below 1 lbf
    max_forces = max_forces[max_forces >= 1]
    
    print("Length of max forces after filtering:", len(max_forces))
    all_max_forces.append(max_forces)

# Create a figure for max force vs cycle number
fig = go.Figure()

all_cycles = []
all_forces = []

for idx, forces in enumerate(all_max_forces):
    cycles = [i + prev_cycles for i in range(1, len(forces) + 1)]
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
    prev_cycles += len(forces)  # Update cumulative cycle count

# Add linear fit across all data
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

print(f"Linear fit: slope = {slope:.6f}, intercept = {intercept:.6f}, r^2 = {r**2:.4f}")
force_at_100k = slope * 100000 + intercept
print(f"Predicted max force at 100,000 cycles: {force_at_100k} lbf")


# Update layout
fig.update_layout(
    title='Max Force vs Cycle Number Across Tests',
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
