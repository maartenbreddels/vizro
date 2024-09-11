############ Imports ##############
import vizro.plotly.express as px
import vizro.tables as vt
import vizro.models as vm
from vizro.models.types import capture
import plotly.express as px
import pandas as pd
import vizro.plotly.express as px
import plotly.graph_objects as go
import vizro.plotly.express as px
from vizro import Vizro
import vizro.models as vm


df1 = pd.read_csv("medallists.csv")
df2 = pd.read_csv("medals_total.csv")


####### Function definitions ######
@capture("graph")
def donut_chart_china(data_frame=None):
    # Make a hard copy of the DataFrame
    df_copy = data_frame.copy()
    # Filter the DataFrame for China
    china_df = df_copy[df_copy["country"] == "China"]
    # Select only the columns for medals
    china_medals = china_df[["Gold Medal", "Silver Medal", "Bronze Medal"]]
    # Reset the index
    china_medals.reset_index(drop=True, inplace=True)
    df = china_medals.reset_index()

    # Data for the donut chart
    medal_counts = df[["Gold Medal", "Silver Medal", "Bronze Medal"]].iloc[0]

    # Create a DataFrame suitable for Plotly
    medal_data = pd.DataFrame(
        {
            "Medal": ["Gold", "Silver", "Bronze"],
            "Count": [
                medal_counts["Gold Medal"],
                medal_counts["Silver Medal"],
                medal_counts["Bronze Medal"],
            ],
        }
    )

    # Create the donut chart
    fig = px.pie(medal_data, values="Count", names="Medal", hole=0.4, title="China")

    # Update layout for better visualization
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(showlegend=True)

    return fig


@capture("graph")
def donut_chart_usa(data_frame=None):
    # Make a hard copy of the DataFrame
    df_copy = data_frame.copy()
    # Filter the DataFrame for the USA
    usa_df = df_copy[df_copy["country_code"] == "USA"]
    # Select only the columns related to medals
    usa_medals = usa_df[["Gold Medal", "Silver Medal", "Bronze Medal"]]
    # Reset the index
    usa_medals.reset_index(drop=True, inplace=True)
    # Rename columns for clarity
    usa_medals.columns = ["Gold", "Silver", "Bronze"]
    df = usa_medals.reset_index()

    # Data for the donut chart
    medal_counts = df[["Gold", "Silver", "Bronze"]].sum()

    # Create a DataFrame for Plotly
    medal_df = pd.DataFrame(
        {"Medal": ["Gold", "Silver", "Bronze"], "Count": medal_counts}
    )

    # Create the donut chart
    fig = px.pie(
        medal_df,
        values="Count",
        names="Medal",
        hole=0.4,
        title="USA",
        # color_discrete_sequence=["#FFD700", "#C0C0C0", "#CD7F32"],
    )

    # Update layout for better appearance
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(showlegend=True)

    return fig


@capture("graph")
def sankey_diagram(data_frame=None):
    df_copy = data_frame.copy()
    # Group by 'discipline' and 'country' and count the number of occurrences
    sankey_data = (
        df_copy.groupby(["discipline", "country"]).size().reset_index(name="count")
    )
    # Ensure the DataFrame is sorted by 'discipline' and 'country'
    sankey_data = sankey_data.sort_values(by=["discipline", "country"]).reset_index(
        drop=True
    )
    df = sankey_data.reset_index()

    # Define the nodes and links for the Sankey diagram
    nodes = list(set(df["discipline"]).union(set(df["country"])))
    node_indices = {node: idx for idx, node in enumerate(nodes)}

    # Create the source and target indices
    sources = df["discipline"].map(node_indices).tolist()
    targets = df["country"].map(node_indices).tolist()
    values = df["count"].tolist()

    # Define colors for the nodes
    colors = [
        "#636EFA" if node in df["discipline"].unique() else "#EF553B" for node in nodes
    ]

    # Create the Sankey diagram
    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=nodes,
                    color=colors,
                ),
                link=dict(source=sources, target=targets, value=values),
            )
        ]
    )

    # Update layout
    fig.update_layout(
        title_text="Sankey Diagram of Medallists by Discipline and Country",
        font_size=10,
    )

    return fig


@capture("graph")
def butterfly_chart(data_frame=None):
    # Make a hard copy of the DataFrame
    df_copy = data_frame.copy()
    # Convert 'birth_date' to datetime
    df_copy["birth_date"] = pd.to_datetime(df_copy["birth_date"])
    # Calculate age
    current_year = 2024
    df_copy["age"] = current_year - df_copy["birth_date"].dt.year
    # Group by gender and age, then count the number of occurrences
    df_age_distribution = (
        df_copy.groupby(["gender", "age"]).size().reset_index(name="count")
    )
    # Pivot the table to have genders as columns
    df_pivot = df_age_distribution.pivot(
        index="age", columns="gender", values="count"
    ).fillna(0)
    # Sort by age
    df_pivot = df_pivot.sort_index()
    df = df_pivot.reset_index()

    # Create the butterfly chart
    fig = go.Figure()

    # Add male bars (negative values for left side)
    fig.add_trace(
        go.Bar(
            y=df["age"],
            x=-df["Male"],
            name="Male",
            orientation="h",
            marker=dict(color="blue"),
        )
    )

    # Add female bars
    fig.add_trace(
        go.Bar(
            y=df["age"],
            x=df["Female"],
            name="Female",
            orientation="h",
            marker=dict(color="pink"),
        )
    )

    # Update layout
    fig.update_layout(
        title="Age Distribution by Gender",
        xaxis_title="Count",
        yaxis_title="Age",
        barmode="relative",
        bargap=0.1,
        xaxis=dict(
            tickvals=[-max(df["Male"]), 0, max(df["Female"])],
            ticktext=[str(max(df["Male"])), "0", str(max(df["Female"]))],
            title="Count",
        ),
        yaxis=dict(title="Age"),
        legend=dict(title="Gender"),
    )

    return fig


@capture("graph")
def donut_chart_japan(data_frame=None):
    # Make a hard copy of the DataFrame
    df_copy = data_frame.copy()
    # Filter the DataFrame for Japan
    japan_df = df_copy[df_copy["country"] == "Japan"]
    # Select only the columns for medals
    japan_medals = japan_df[["Gold Medal", "Silver Medal", "Bronze Medal"]]
    # Reset the index
    japan_medals.reset_index(drop=True, inplace=True)
    # Rename the columns for clarity
    japan_medals.columns = ["Gold", "Silver", "Bronze"]
    # Display the DataFrame for verification
    df = japan_medals.reset_index()

    # Data for the donut chart
    medal_counts = df[["Gold", "Silver", "Bronze"]].sum()

    # Create a DataFrame for the medal counts
    medal_df = pd.DataFrame(
        {"Medal": ["Gold", "Silver", "Bronze"], "Count": medal_counts}
    )

    # Create the donut chart
    fig = px.pie(medal_df, values="Count", names="Medal", hole=0.4, title="Japan")

    # Update layout for better visualization
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(showlegend=True)

    return fig


####### Data Manager Settings #####
#######!!! UNCOMMENT BELOW !!!#####
from vizro.managers import data_manager
data_manager["df5d08b1-ec51-4e66-9311-272f71489221"] = df2
data_manager["5b57d30d-c4b3-4b4f-b641-774a8b9c54b7"] = df1
data_manager["2f5bae96-ca94-4e71-94d6-ea5171ea9fe3"] = df2
data_manager["4a5c3d00-397e-476a-ad08-1ddf6197f01a"] = df1
data_manager["medal_distribution"] = df2
data_manager["d721fef6-1298-47b8-848f-e53723cb540c"] = df2


########### Model code ############
model = vm.Dashboard(
    pages=[
        vm.Page(
            components=[
                vm.Graph(
                    id="butterfly_chart",
                    figure=butterfly_chart(
                        data_frame="4a5c3d00-397e-476a-ad08-1ddf6197f01a"
                    ),
                ),
                vm.Graph(
                    id="sankey_diagram",
                    figure=sankey_diagram(
                        data_frame="5b57d30d-c4b3-4b4f-b641-774a8b9c54b7"
                    ),
                ),
            ],
            title="Medal Distribution and Age Comparison",
            layout=vm.Layout(grid=[[0, 1]]),
            controls=[
                vm.Filter(
                    column="medal_type",
                    targets=["butterfly_chart", "sankey_diagram"],
                    selector=vm.RadioItems(type="radio_items"),
                ),
                vm.Filter(
                    column="discipline", targets=["butterfly_chart", "sankey_diagram"]
                ),
            ],
        ),
        vm.Page(
            components=[
                vm.Graph(
                    id="donut_chart_usa",
                    figure=donut_chart_usa(
                        data_frame="d721fef6-1298-47b8-848f-e53723cb540c"
                    ),
                ),
                vm.Graph(
                    id="donut_chart_china",
                    figure=donut_chart_china(
                        data_frame="2f5bae96-ca94-4e71-94d6-ea5171ea9fe3"
                    ),
                ),
                vm.Graph(
                    id="donut_chart_japan",
                    figure=donut_chart_japan(
                        data_frame="df5d08b1-ec51-4e66-9311-272f71489221"
                    ),
                ),
                vm.Card(
                    id="highlights_card",
                    type="card",
                    text='Highlights: Some notable highlights from the Games include Novak Djokovic winning the gold medal in men\'s singles tennis, completing the Career Golden Slam and becoming the only man to win all "Big Titles" in singles. In swimming, 17-year-old Canadian Summer McIntosh emerged as a standout star, winning three gold medals and one silver.',
                    href="",
                ),
                vm.AgGrid(
                    id="medal_table",
                    figure=vt.dash_ag_grid(data_frame="medal_distribution"),
                ),
            ],
            title="Medal Counts and Highlights",
            layout=vm.Layout(grid=[[0, 1, 2, 3, 3, 3], [4, 4, 4, 4, 4, 4]]),
            controls=[],
        ),
    ],
    title="Olympic Medals Dashboard",
)
Vizro().build(model).run(port=8070)