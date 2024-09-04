import dash_bootstrap_components as dbc

import subprocess
from actions import data_upload_action, display_filename
import vizro.models as vm
from components import (
    CodeClipboard,
    MyDropdown,
    MyPage,
    OffCanvas,
    UserPromptTextArea,
    UserUpload,
    CustomDashboard,
    Icon
)

from dash.exceptions import PreventUpdate
from dash import Input, Output, State, callback, get_asset_url, html
from dash.exceptions import PreventUpdate
from vizro import Vizro

SUPPORTED_MODELS = [
    "gpt-4o-mini",
    "gpt-4",
    "gpt-4-turbo",
    "gpt-3.5-turbo",
    "gpt-4o",
]
vm.Container.add_type("components", UserUpload)
vm.Container.add_type("components", MyDropdown)
vm.Container.add_type("components", OffCanvas)
vm.Container.add_type("components", CodeClipboard)
vm.Container.add_type("components", Icon)

MyPage.add_type("components", UserPromptTextArea)
MyPage.add_type("components", UserUpload)
MyPage.add_type("components", MyDropdown)
MyPage.add_type("components", OffCanvas)
MyPage.add_type("components", CodeClipboard)
MyPage.add_type("components", Icon)

dashboard_page = MyPage(
    id="vizro_ai_dashboard_page",
    title="Vizro AI - Dashboard",
    layout=vm.Layout(
        # grid=[
        #     *[[0, 0, 0, 0]] * 6,
        #     [1, 1, 1, 1],
        #     [2, 2, 2, 2],
        #     [3, 3, 3, 3],
        # ]
        grid=[
            [2, 2, 0, 0, 0],
            [1, 1, 0, 0, 0],
            [1, 1, 0, 0, 0],
            [3, 3, 0, 0, 0]

        ]
    ),
    components=[
        vm.Container(title="", components=[CodeClipboard(id="dashboard")]),
        UserPromptTextArea(
            id="dashboard-text-area",
        ),
        vm.Container(
            title="",
            layout=vm.Layout(grid=[[0], [1]], row_gap="0px"),
            components=[
                UserUpload(
                    id="dashboard-data-upload",
                    actions=[
                        vm.Action(
                            function=data_upload_action(),
                            inputs=["dashboard-data-upload.contents", "dashboard-data-upload.filename"],
                            outputs=["dashboard-data-store.data"],
                        ),
                        vm.Action(
                            function=display_filename(),
                            inputs=["dashboard-data-store.data"],
                            outputs=["dashboard-upload-message-id.children"],
                        ),
                    ],
                ),
                vm.Card(id="dashboard-upload-message-id", text="Upload your data files (csv or excel)"),
            ],
        ),
        vm.Container(
            title="",
            layout=vm.Layout(grid=[[0, 0, 1, 1, -1, -1, -1, 2, 3]], row_gap="0px", col_gap="4px"),
            components=[
                vm.Button(
                    id="dashboard-trigger-button",
                    text="Run VizroAI",
                ),
                MyDropdown(options=SUPPORTED_MODELS, value="gpt-3.5-turbo", multi=False, id="dashboard-model-dropdown"),
                vm.Button(id="dashboard-open_settings", text="Settings"),
                OffCanvas(id="dashboard-settings", options=["ChatOpenAI"], value="ChatOpenAI"),
            ],
        ),
    ],
)

dashboard = CustomDashboard(pages=[dashboard_page])


@callback(
    [Output("dashboard-api-store", "data"), Output("dashboard-offcanvas-id_notification", "children")],
    [
        Input("dashboard-offcanvas-id_api_key", "value"),
        Input("dashboard-offcanvas-id_api_base", "value"),
        Input("dashboard-offcanvas-id_save-secrets-id", "n_clicks"),
    ],
)
def save_dashboard_secrets(api_key, api_base, n_clicks):
    if not n_clicks:
        raise PreventUpdate

    if api_key and api_base:
        return {"api_key": api_key, "api_base": api_base}, "Secrets saved!"


@callback(
    [Output("dashboard-offcanvas-id_api_key", "type"), Output("dashboard-offcanvas-id_api_base", "type")],
    Input("dashboard-offcanvas-id_toggle-secrets-id", "value"),
)
def show_secrets(value):
    return ("text", "text") if value else ("password", "password")


@callback(
    Output("dashboard-offcanvas-id", "is_open"),
    Input("dashboard-open_canvas", "n_clicks"),
    [State("dashboard-offcanvas-id", "is_open")],
)
def toggle_offcanvas(n_clicks, is_open):
    return not is_open if n_clicks else is_open


@callback(
    [
        Output("dashboard_code-markdown", "children", allow_duplicate=True),
        Output("dashboard-text-area", "value"),
        Output("dashboard-upload-message-id", "children"),
    ],
    [Input("on_page_load_action_trigger_vizro_ai_plot_dashboard", "data")],
    [State("dashboard-outputs-store", "data")],
    prevent_initial_call="initial_duplicate",
)
def update_data(page_data, outputs_data):
    if not outputs_data:
        raise PreventUpdate

    ai_response = outputs_data["ai_response"]
    filename = f"Uploaded file name: '{outputs_data['filename']}'"
    prompt = outputs_data["prompt"]

    return ai_response, prompt, filename


@callback(
    [
        Output('dashboard-code-markdown', 'children'),
        # Output('dashboard-outputs-store', 'data'),
     ],
    [
        Input('dashboard-trigger-button', 'n_clicks'),
        Input('dashboard-text-area', 'value'),
        Input('dashboard-data-store-id', 'data'),
        Input('dashboard-model-dropdown', 'value'),
        Input('dashboard-api-store-id', 'data'),
    ]
)
def run_script(n_clicks, user_prompt, data_store, model, api_store):
    if n_clicks is None:
        return "Click the button to run the script."
    else:
        # Run the other Python script
        result = subprocess.run([
            'python', 'run_vizroai.py', '--arg1', 'user_prompt', '--arg2', 'data_store',  '--arg3', 'model', '--arg4', 'api_store', '--arg5', 'n_clicks'
        ], capture_output=True, text=True)
        return f"Script output: {result.stdout}"




app = Vizro().build(dashboard)
app.dash.layout.children.append(
    html.Div(
        [
            dbc.NavLink("Contact us", href="https://github.com/mckinsey/vizro/issues"),
            dbc.NavLink("GitHub", href="https://github.com/mckinsey/vizro"),
            dbc.NavLink("Docs", href="https://vizro.readthedocs.io/projects/vizro-ai/"),
            html.Div(
                [
                    "Made using ",
                    html.Img(src=get_asset_url("logo.svg"), id="banner", alt="Vizro logo"),
                    "vizro",
                ],
            ),
        ],
        className="anchor-container",
    )
)


if __name__ == "__main__":
    app.run()