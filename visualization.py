import pandas as pd
import plotly.express as px

df = pd.read_csv("calculations.csv")

bins = range(
    0, 2400, 200
)  

labels = [f"{i}-{i + 200}" for i in bins[:-1]]
df["elevation_bin"] = pd.cut(df["elevation"], bins=bins, labels=labels, right=True)
avg_grad_by_elevation = df.groupby("elevation_bin")["avg_grad"].mean().reset_index()


fig = px.line(
    avg_grad_by_elevation,
    x="elevation_bin",
    y="avg_grad",
    title="Average Graduation Rate by Elevation Bins",
    markers=True
)

fig.update_traces(line_color="blue")
fig.update_layout(
    plot_bgcolor="#343d46", 
    paper_bgcolor="whitesmoke", 
    xaxis_title="Elevation",
    yaxis_title="Average Graduation Rate"
)
fig.update_xaxes(linewidth=0.1, gridcolor="#4f5b66")
fig.update_yaxes(linewidth=0.1, gridcolor="#4f5b66")
fig.show()
