import pandas as pd
import plotly.express as px

# Load data from CSV file
df = pd.read_csv("calculations.csv")

# Define bins for elevation
bins = range(
    0, 2400, 200
)  

labels = [f"{i}-{i + 200}" for i in bins[:-1]]
df["elevation_bin"] = pd.cut(df["elevation"], bins=bins, labels=labels, right=True)

# Calculate average graduation rate by elevation bin
avg_grad_by_elevation = df.groupby("elevation_bin")["avg_grad"].mean().reset_index()
print(avg_grad_by_elevation)
# Create a line graph
fig = px.line(
    avg_grad_by_elevation,
    x="elevation_bin",
    y="avg_grad",
    title="Average Graduation Rate by Elevation Bins",
)

fig.show()
