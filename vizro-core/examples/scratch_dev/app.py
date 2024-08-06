from typing import List, Optional

import pandas as pd
import plotly.graph_objects as go
import vizro.models as vm
import vizro.plotly.express as px
from plotly.subplots import make_subplots
from vizro import Vizro
from vizro._themes._color_values import COLORS
from vizro.actions import filter_interaction
from vizro.models.types import capture

df = pd.read_csv("linkedin_input_data.csv")
df.dropna(subset=["Position", "Company"], inplace=True)
df["Connected On"] = pd.to_datetime(df["Connected On"], format="%d-%b-%y")
df.set_index("Connected On", drop=False, inplace=True)
df["Year"] = df["Connected On"].dt.year


@capture("graph")
def role_bar_chart(data_frame, top_n=5, custom_data: Optional[List[str]] = None):
    data_frame = data_frame["Position"].value_counts().nlargest(top_n).reset_index(name="Frequency")
    data_frame = data_frame.sort_values(by="Frequency", ascending=True)

    fig = px.bar(
        data_frame,
        x="Frequency",
        y="Position",
        title=f"Top {top_n} positions of my connections 💼"
        + "<br><sup> ⤵ Click on bar to filter charts on the right. Refresh the page to deselect.</sup>",
        custom_data=custom_data,
    )
    fig.update_layout(xaxis_title="Number of people", title_pad_t=24)
    return fig


@capture("graph")
def company_pie_chart(data_frame, top_n=5):
    # Calculate top n companies based on counts and categorize all others into "Other"
    top_n_companies = data_frame["Company"].value_counts().nlargest(top_n).index
    data_frame["Company"] = data_frame["Company"].apply(lambda x: x if x in top_n_companies else "Others")
    df_agg = data_frame["Company"].value_counts().reset_index()

    title_with_subtitle = (
        f"Top {top_n} most connected companies 🏢</span><br><span style='font-size: 14px;'>Shows top {top_n} "
        f"companies by connections, with all others grouped as 'Others'</span>"
    )
    fig = px.pie(
        df_agg,
        names="Company",
        values="count",
        color_discrete_sequence=["rgba(108, 122, 137, 0.3)"] + COLORS["DISCRETE_10"],
        hole=0.4,
    )
    fig.update_layout(legend=dict(x=1, y=1, orientation="v"), title=title_with_subtitle, title_pad_t=24)
    return fig


@capture("graph")
def growth_cumulative_chart(data_frame):
    data_frame = data_frame.groupby("Year").size().reset_index(name="Count per Year")
    data_frame["Cumulative Yearly Connections"] = data_frame["Count per Year"].cumsum()

    # Create dual y-axes chart and synchronize range of axes
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(x=data_frame["Year"], y=data_frame["Count per Year"], name="Per Year Connections"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=data_frame["Year"],
            y=data_frame["Cumulative Yearly Connections"],
            name="Cumulative Connections",
        ),
        secondary_y=True,
    )
    fig.update_layout(
        title="Per Year and Cumulative Connections 📈",
        yaxis=dict(tickmode="sync", title=dict(text="Per Year Connections [Bar]", font_size=14)),
        yaxis2=dict(tickmode="sync", overlaying="y", title=dict(text="Cumulative Connections [Line]", font_size=14)),
    )
    return fig


page = vm.Page(
    title="My LinkedIn connections",
    layout=vm.Layout(grid=[[0, 1], [0, 2]]),
    components=[
        vm.Graph(
            id="role_bar_chart_id",
            figure=role_bar_chart(data_frame=df, custom_data=["Position"]),
            actions=[
                vm.Action(function=filter_interaction(targets=["company_pie_chart_id", "growth_cumulative_chart_id"]))
            ],
        ),
        vm.Graph(id="company_pie_chart_id", figure=company_pie_chart(data_frame=df)),
        vm.Graph(id="growth_cumulative_chart_id", figure=growth_cumulative_chart(data_frame=df)),
    ],
    controls=[
        vm.Filter(column="Company"),
        vm.Filter(column="Year", selector=vm.RangeSlider(step=1, marks=None)),
        vm.Parameter(
            targets=["role_bar_chart_id.top_n"],
            selector=vm.Slider(min=0, max=30, step=5, value=25, title="Show top n positions:"),
        ),
        vm.Parameter(
            targets=["company_pie_chart_id.top_n"],
            selector=vm.Slider(min=1, max=10, step=1, value=5, title="Show top n companies:"),
        ),
    ],
)

dashboard = vm.Dashboard(pages=[page], theme="vizro_light")
Vizro().build(dashboard).run()
