"""Dev app to try things out."""
import vizro.models as vm
import vizro.plotly.express as px
import plotly.graph_objects as go
from vizro import Vizro
from vizro.tables import dash_ag_grid
from dash import Input, Output, State, callback, no_update, ctx
import pandas as pd

df = pd.DataFrame({
    "date": pd.Series(dtype="datetime64[ns]"),
    "value": pd.Series(dtype="float")
})

columnDefs = [
    {"headerName": "Date", "field": "date", "editable": True, "cellEditor": "datePicker","checkboxSelection": True},
    {"headerName": "Value", "field": "value", "editable": True, "cellEditor": "numericEditor"},
]

empty_figure = go.Figure(
                    layout={
                        "title": "Timeline of input data",
                        "paper_bgcolor": "rgba(0,0,0,0)",
                        "plot_bgcolor": "rgba(0,0,0,0)",
                        "xaxis": {"visible": False},
                        "yaxis": {"visible": False},
                    }
                )

#update the chart based on the edited table
@callback(
    Output("output_chart", "figure", allow_duplicate=True),
    Input("__input_editing-grid2", "cellValueChanged"),
    Input("__input_editing-grid2", "rowData"),
    Input("theme_selector", "checked"),
    prevent_initial_call=True
)
def update(_, rows,theme_selector):
    dff = pd.DataFrame(rows)
    if dff.empty:
        return empty_figure
    fig = px.line(dff,title = "Timeline of input data", x="date", y="value")
    fig.update_layout(template="vizro_light" if theme_selector else "vizro_dark") #to get the theme right
    return fig

# add or delete rows of table
@callback(
    Output("__input_editing-grid2", "deleteSelectedRows"),
    Output("__input_editing-grid2", "rowData"),
    Input("delete-row-btn", "n_clicks"),
    Input("add-row-btn", "n_clicks"),
    State("__input_editing-grid2", "rowData"),
    prevent_initial_call=True,
)
def update_dash_table(n_dlt, n_add, data):
    if ctx.triggered_id == "add-row-btn":
        new_row = {
            "date": ["2020-01-01"],
            "value": [0.0]
        }
        df_new_row = pd.DataFrame(new_row)
        updated_table = pd.concat([pd.DataFrame(data), df_new_row])
        return False, updated_table.to_dict("records")

    elif ctx.triggered_id == "delete-row-btn":
        return True, no_update

page = vm.Page(
    title="Example of adding rows to AG Grid and updating a chart based on the edited table",
    layout=vm.Layout(grid = [
        [0,0,0,0,1,1,1,1],
        [0,0,0,0,1,1,1,1],
        [0,0,0,0,1,1,1,1],
        [2,3,-1,-1,-1,-1,-1,-1],
        ] ),
    components=[
        vm.AgGrid(
            id = "editing-grid2",
            title="Editable Table / AG Grid",
            figure=dash_ag_grid(
                data_frame=df,
                columnDefs=columnDefs,
                defaultColDef={"editable": True},
                columnSize="sizeToFit",
                dashGridOptions={"rowSelection": "multiple", "suppressRowClickSelection": True},
            ),
        ),
        vm.Graph(id = "output_chart",figure = px.line(df, title = "Timeline of input data",x="date", y="value")),
        vm.Button(
            id="delete-row-btn",
            text="Delete row",
        ),
        vm.Button(
            id="add-row-btn",
            text="Add row",
        ),
    ],
)

dashboard = vm.Dashboard(pages=[page])

Vizro().build(dashboard).run(debug=True)