import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__)

periods = ["last 6 months", "last month", "last week", "last day", "last hour"]
stations = ["Trento - via Bolzano", "Trento - S. Chiara"]
points = {
    (11.11022, 46.10433): "Trento - via Bolzano",
    (11.1262, 46.06292): "Trento - S. Chiara",
}
pollutants = ["NO2", "O3", "CO", "PM 2.5", "PM 10",]

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
    style={},
)


####################
# POLLUTANT LEVELS #
####################

def select_color(value):
    if value < 30:
        return "Success"
    elif value < 60:
        return "Warning"
    else:
        return "Danger"

progress_bars = html.Div(
    [
        html.Div(
            [
                html.Div("NO2", className="progress-label"),
                dbc.Progress(
                    id="no2-progress",
                    value=90,
                    max=100,
                    striped=True,
                    animated=True,
                    color="Danger",
                    className="mb-3 font-size",

                ),
                html.Div("O3", className="progress-label"),
                dbc.Progress(
                    id="o3-progress",
                    value=80,
                    max=100,
                    striped=True,
                    animated=True,
                    color="warning",
                    className="mb-3",
                ),
                html.Div("CO", className="progress-label"),
                dbc.Progress(
                    id="co2-progress",
                    value=20,
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

question_icon = html.Div(
    [
        dbc.Tooltip(
            """
            Placeholder
            """,
            target="question-icon",
            style={"font-size": "1.5rem"}
        ),
        html.I(
            className="fa-solid fa-question-circle fa-2x",
            id="question-icon",
            n_clicks=0,
            style={"cursor": "pointer"},
        ),
    ],
    className="question-icon-container",
)

toast = dbc.Toast(
    [progress_bars],
    id="pollutants",
    style={"height": "100%"},
    header=dbc.Row([
           html.H4(
                "Gas Pollutants",
                className="section-header",
                style={"alignItem": "right"},
            ),
            question_icon,
        ],
        class_name="row",
    ),
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
        toast,
    ]
)
