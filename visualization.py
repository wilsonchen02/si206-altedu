import pandas as pd
import plotly.express as px

def bar_graph(df):
    df["student_percentage"] = (
        df["student_percentage"].str.replace("%", "").astype(float)
    )
    df = df[df["student_percentage"] < 100]
    df = df.sort_values(by="student_percentage", ascending=True)
    fig = px.bar(
        df, x="city", y="student_percentage", title="Student Percentage by City"
    )
    fig.update_layout(
        xaxis_title="City",
        yaxis_title="Student Percentage",
        plot_bgcolor="lightgray",  # Optional: Change the plot background color
        paper_bgcolor="whitesmoke",  # Optional: Change the overall figure background color
    )
    fig.update_layout(
        plot_bgcolor="#343d46", 
        paper_bgcolor="whitesmoke", 
        xaxis_title="City Name",
        yaxis_title="Student Percentage"
    )
    fig.update_xaxes(linewidth=0.1, gridcolor="#4f5b66")
    fig.update_yaxes(linewidth=0.1, gridcolor="#4f5b66")
    fig.update_traces(marker_color="blue")

    fig.show()

def histogram(df):
    bins = range(
        0, 2400, 200
    )  

    labels = [f"{i}-{i + 200}" for i in bins[:-1]]
    df["elevation_bin"] = pd.cut(df["elevation"], bins=bins, labels=labels, right=True)
    avg_grad_by_elevation = df.groupby("elevation_bin")["avg_grad"].mean().reset_index()

    fig = px.histogram(
        avg_grad_by_elevation,
        x="elevation_bin",
        y="avg_grad",
        title="Average Graduation Rate by Elevation Bins",
        color_discrete_sequence=["blue"]
    )
    
    fig.update_layout(
        bargap=0.03,
        xaxis_title="Elevation of City (m)",
        yaxis_title="Average Graduation Rate of Students in City"
    )

    # fig = px.line(
    #     avg_grad_by_elevation,
    #     x="elevation_bin",
    #     y="avg_grad",
    #     title="Average Graduation Rate by Elevation Bins",
    #     markers=True
    # )

    # fig.update_traces(line_color="blue")
    # fig.update_layout(
    #     plot_bgcolor="#343d46", 
    #     paper_bgcolor="whitesmoke", 
    #     xaxis_title="Elevation",
    #     yaxis_title="Average Graduation Rate"
    # )
    # fig.update_xaxes(linewidth=0.1, gridcolor="#4f5b66")
    # fig.update_yaxes(linewidth=0.1, gridcolor="#4f5b66")
    fig.show()

def main():
    df = pd.read_csv("calculations.csv")
    histogram(df)
    bar_graph(df)


if __name__ == "__main__":
    main()
