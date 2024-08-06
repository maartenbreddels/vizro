"""Dev app to try things out."""

import random

import pandas as pd
import vizro.models as vm
import vizro.plotly.express as px
from vizro import Vizro
from vizro._themes._color_values import COLORS
from vizro.models.types import capture

# Load the data
df = pd.read_csv("linkedin_input_data.csv")

# Clean the data
df.dropna(subset=["Position", "Company"], inplace=True)
df["Connected On"] = pd.to_datetime(df["Connected On"], format="%d-%b-%y")
df.set_index("Connected On", drop=False, inplace=True)
df["Year"] = df["Connected On"].dt.year

icons = ["👨", "👩", "👧", "👦", "🧒"]


@capture("graph")
def role_chart(data_frame, top_n=5):
    # Sample data preparation
    data_frame = data_frame["Position"].value_counts().nlargest(top_n).reset_index(name="Frequency")
    data_frame = data_frame.sort_values(by="Frequency", ascending=True)

    # Create a new DataFrame to hold the dots
    dot_list = []
    for i, row in data_frame.iterrows():
        dot_list.append(
            pd.DataFrame(
                {
                    "Position": [row["Position"]] * row["Frequency"],
                    "Frequency": list(range(1, row["Frequency"] + 1)),
                    "Icon": [random.choice(icons) for _ in range(row["Frequency"])],
                }
            )
        )
    dots_df = pd.concat(dot_list, ignore_index=True)

    fig = px.scatter(dots_df, x="Frequency", y="Position", title=f"Top {top_n} most frequent positions", text="Icon")
    fig.update_layout(yaxis=dict(showgrid=False))

    return fig


@capture("graph")
def company_chart(data_frame, top_n=10):
    title_with_subtitle = (
        f"Top {top_n} most connected companies 💼</span><br>"
        + f"<span style='font-size: 14px;'>Shows top {top_n} companies by connections, with all others grouped as 'Others'</span>"
    )

    # Calculate top n companies based on counts and recategorize all others into "Other"
    top_n_companies = data_frame["Company"].value_counts().nlargest(top_n).index
    data_frame["company_with_other"] = data_frame["Company"].apply(lambda x: x if x in top_n_companies else "Others")
    df_agg = data_frame["company_with_other"].value_counts().reset_index()

    # Plot a pie chart
    fig = px.pie(
        df_agg,
        names="company_with_other",
        values="count",
        color_discrete_sequence=["rgba(108, 122, 137, 0.3)"] + COLORS["DISCRETE_10"],
        hole=0.4,
    )
    fig.update_layout(legend=dict(x=1, y=1, orientation="v"), title=title_with_subtitle, title_pad_t=24)
    return fig


@capture("graph")
def growth_cumulative_chart(data_frame):
    # Plot the growth of my connections over time
    data_frame = data_frame.groupby("Year").size().reset_index(name="Count per Year")
    data_frame["Cumulative Yearly Connections"] = data_frame["Count per Year"].cumsum()

    line_fig = px.line(
        data_frame, x="Year", y="Cumulative Yearly Connections", color=px.Constant("Cumulative Connections")
    )
    line_fig.update_traces(yaxis="y2", line_color="#F08D41")

    bar_fig = px.bar(
        data_frame,
        x="Year",
        y="Count per Year",
        color=px.Constant("Count per Year"),
        title="Yearly growth of my connections",
    )
    bar_fig.add_traces(line_fig.data)

    bar_fig.update_layout(
        yaxis=dict(title="Per Year Connections [Bar]"),
        yaxis2=dict(title="Cumulative Connections [Line]", overlaying="y", side="right"),
        legend=dict(title="", yanchor="bottom", y=1, xanchor="right", x=1),
    )

    return bar_fig


page = vm.Page(
    title="LinkedIn data",
    layout=vm.Layout(grid=[[0, 1], [0, 2]]),
    components=[
        vm.Graph(id="role_chart_id", figure=role_chart(data_frame=df)),
        vm.Graph(id="company_chart_id", figure=company_chart(data_frame=df)),
        vm.Graph(figure=growth_cumulative_chart(data_frame=df)),
    ],
    controls=[
        vm.Filter(
            column="Position",
            selector=vm.Dropdown(options=df["Position"].value_counts().loc[lambda x: x >= 5].index.tolist()),
        ),
        vm.Filter(column="Company"),
        vm.Parameter(
            targets=["role_chart_id.top_n"],
            selector=vm.Slider(
                min=1, max=30, step=1, marks={1: "1", 10: "10", 20: "20", 30: "30"}, value=30, title="Top N roles"
            ),
        ),
        vm.Parameter(
            targets=["company_chart_id.top_n"],
            selector=vm.Slider(min=1, max=10, step=1, value=5, title="Top N companies"),
        ),
        vm.Filter(column="Year", selector=vm.RangeSlider(step=1, marks=None)),
    ],
)

dashboard = vm.Dashboard(pages=[page], theme="vizro_light")

if __name__ == "__main__":
    Vizro().build(dashboard).run()
