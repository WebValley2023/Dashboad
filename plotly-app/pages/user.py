import dash
from dash import html, dcc, dash_table, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

dash.register_page(__name__)

periods = ["last 6 months", "last month", "last week", "last day", "last hour"]
stations = ["Trento - via Bolzano", "Trento - S. Chiara"]
points = {
    (11.11022, 46.10433): "Trento - via Bolzano",
    (11.1262, 46.06292): "Trento - S. Chiara",
}
pollutants = [
    dict(label="Nitrogen Dioxide", value="NO2"),
    dict(label="Ozone", value="O3"),
    dict(label="Carbon Monoxide", value="CO"),
]

gas_btns = html.Div(
    dbc.RadioItems(
        id="selected-fbk-pollutant",
        class_name="btn-group",
        input_class_name="btn-check",
        label_class_name="btn btn-outline-primary",
        label_checked_class_name="active",
        options=pollutants,
        value="NO2",
    ),
    className="radio-group",
)

progress_bars = html.Div(
    [
        html.Div(
            [
                html.Div("NO2", className="progress-label"),
                dbc.Progress(
                    id="no2-progress",
                    value=0,
                    max=100,
                    striped=True,
                    animated=True,
                    color="danger",
                    className="mb-3",
                ),
                html.Div("O3", className="progress-label"),
                dbc.Progress(
                    id="o3-progress",
                    value=0,
                    max=100,
                    striped=True,
                    animated=True,
                    color="warning",
                    className="mb-3",
                ),
                html.Div("CO", className="progress-label"),
                dbc.Progress(
                    id="co2-progress",
                    value=0,
                    max=100,
                    striped=True,
                    animated=True,
                    color="success",
                    className="mb-3",
                ),
            ],
            className="progress-container",
        ),
    ],
    className="post-box",
)

description = """
This is the description of the gas pollutants. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
"""

popup_menu = dbc.Modal(
    [
        dbc.ModalHeader("Gas Pollutants Description"),
        dbc.ModalBody(description),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-popup", className="ml-auto", n_clicks=0)
        ),
    ],
    id="popup-menu",
    size="lg",
)

info_icon = html.Div(
    [
        dbc.Tooltip("Click for Description", target="info-icon"),
        html.I(
            className="fa-solid fa-info-circle fa-2x",
            id="info-icon",
            n_clicks=0,
            style={"cursor": "pointer"},
        ),
    ],
    className="info-icon-container",
)

toast = dbc.Toast(
    [
        html.Div(
            className="title-container",
        ),
        progress_bars,
    ],
    id="pollutants",
    header=[html.H4("Gas Pollutants", className="section-header"), info_icon],
    style={"height": "100%"},
)

layout = html.Div(
    children=[
        html.Label("Select Location:"),
        dcc.Dropdown(
            options=[{"label": station, "value": station} for station in stations],
            id="location-dropdown",
            value="Trento - via Bolzano",
            className="dropdown",
        ),
        gas_btns,
        dbc.Row(
            [
                dbc.Col(
                    [toast],
                    width=4),
                dbc.Col(
                    [toast],
                    width=4),
                dbc.Col(
                    [toast],
                    width=4),
            ],
        ),
        popup_menu,
    ],   
)


@callback(
    Output("popup-menu", "is_open"),
    [Input("question-icon", "n_clicks"), Input("close-popup", "n_clicks")],
    [State("popup-menu", "is_open")],
)
def toggle_popup(n_clicks_open, n_clicks_close, is_open):
    if n_clicks_open or n_clicks_close:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True)
