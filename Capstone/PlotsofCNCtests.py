import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import os

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

# Load and plot each CSV file with linear progression
x_offset = 0
cycle_boundaries = [0]  # Track where each cycle starts

for idx, csv_file in enumerate(csv_files):
    df = pd.read_csv(csv_file, skiprows=2)  # Skip header and units row
    
    # Rename columns to be the actual names
    df.columns = ['Time', 'Displacement', 'Force']
    
    # Convert to numeric (remove any quotes)
    df['Time'] = pd.to_numeric(df['Time'], errors='coerce')
    df['Force'] = pd.to_numeric(df['Force'], errors='coerce')
    
    # Extract cycle number from filename
    cycle_num = idx + 1
    
    # Get the duration of this cycle
    cycle_duration = df['Time'].max()
    
    # Offset the time values for linear progression
    adjusted_time = df['Time'] + x_offset
    
    # Add trace for this cycle
    fig.add_trace(go.Scatter(
        x=adjusted_time,
        y=df['Force'],
        mode='lines',
        name=f'Cycle {cycle_num}',
        line=dict(
            color=colors[idx % len(colors)],
            width=2
        ),
        hovertemplate='<b>Cycle %{fullData.name}</b><br>Time: %{x:.4f} s<br>Force: %{y:.4f} lbf<extra></extra>'
    ))
    
    # Update offset for next cycle
    x_offset += cycle_duration
    cycle_boundaries.append(x_offset)

# Update layout for better interactivity
fig.update_layout(
    title=f'Spring Stress Cycles - Force vs Time (Linear Progression - Total Cycles: {len(csv_files)})',
    xaxis_title='Cycles (s)',
    yaxis_title='Force (lbf)',
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

# Add vertical lines to mark cycle boundaries
for i, boundary in enumerate(cycle_boundaries[1:], 1):
    fig.add_vline(
        x=boundary,
        line_dash='dash',
        line_color='gray',
        opacity=0.5,
        annotation_text=f'Cycle {i} → {i+1}',
        annotation_position='top'
    )

# Add range slider to see force degradation over time
fig.update_xaxes(rangeslider_visible=False)

# Show the plot
fig.show()

# Optionally save the plot
output_file = Path(__file__).parent / 'CNC_Delrin_Tests_Interactive.html'
fig.write_html(str(output_file))
print(f"Interactive plot saved to: {output_file}")
