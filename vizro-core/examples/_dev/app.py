from vizro import Vizro
import vizro.plotly.express as px
import vizro.models as vm
from vizro.managers import data_manager
from dash import callback, Input, Output
import pandas as pd

@callback(
    Output('print', 'children'),
    [Input('url', 'search')])
def callback_func(search):
    print(search)
    return search


# define a data connector
def retrieve_iris():
    """This is a function that returns a Pandas DataFrame."""
    return pd.read_csv("iris1.csv")

# register the data connector with Vizro Data Manager
data_manager["iris"] = retrieve_iris

page = vm.Page(
    title="My first page",
    components=[
        vm.Graph(id="scatter_chart", figure=px.scatter("iris", x="sepal_length", y="petal_width", color="species")),
    ],
    controls=[vm.Filter(column="species")],
)

page2 = vm.Page(
    title="My second page",
    components=[
        vm.Graph(id="scatter_chart2", figure=px.scatter("iris", x="sepal_length", y="petal_width", color="species")),
    ],
    controls=[vm.Filter(column="species")],
)

dashboard = vm.Dashboard(pages=[page, page2])

Vizro().build(dashboard).run()