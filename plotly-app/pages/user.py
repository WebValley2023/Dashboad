import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from db_utils import load_data_from_psql
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np


dash.register_page(__name__, path="/user")
description_box = html.Div(id="description-box", className="description-box")


periods = ["last 6 months", "last month", "last week", "last day", "last hour"]
stations = ["Trento - via Bolzano", "Trento - S. Chiara"]
station_labels_to_df_keys = {
    "Trento - via Bolzano": "Via Bolzano",
    "Trento - S. Chiara": "Parco S. Chiara",
}

points = {
    (11.11022, 46.10433): "Trento - via Bolzano",
    (11.1262, 46.06292): "Trento - S. Chiara",
}
pollutants = [
    dict(label="Nitrogen Dioxide", value="NO2"),
    dict(label="Ozone", value="O3"),
    dict(label="Carbon Monoxide", value="CO"),
    dict(label="Particulate Matter 2.5", value="PM2.5"),
    dict(label="Particulate Matter 10", value="PM10"),
]
df = load_data_from_psql(
    """select stazione, inquinante, ts, valore from 
    appa_data where ts >= NOW() - interval '1 month';"""
)
# df_stations = {
#     s: {
#         p: df[(df.stazione == s) & (df.inquinante == p)].copy() for p in df[df.stazione == s].inquinante.drop_duplicates().values
#     }
#     for s in df.stazione.drop_duplicates().values
# }

df_s_p = df.sort_values(["stazione", "inquinante", "ts"]).set_index(
    ["stazione", "inquinante"]
)

print(df)


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

pollutants_bars = html.Div(
    [
        html.Div(
            [
                html.Div("NO2", className="progress-label", style={"fontSize": "1.35rem"}),
                dbc.Progress(
                    id="no2-progress",
                    value=50,
                    striped=True,
                    animated=True,
                    color="danger",
                    className="mb-3",
                ),
            ],
            className="progress-container",
        ),
        html.Div(
            [
                html.Div("O3", className="progress-label", style={"fontSize": "1.35rem"}),
                dbc.Progress(
                    id="o3-progress",
                    value=40,
                    max=100,
                    striped=True,
                    animated=True,
                    color="warning",
                    className="mb-3",
                ),
            ],
            className="progress-container",
        ),
        html.Div(
            [
                html.Div("CO", className="progress-label", style={"fontSize": "1.35rem"}),
                dbc.Progress(
                    id="co2-progress",
                    value=50,
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

pm_bars = html.Div(
    [
        html.Div(
            [
                html.Div("PM 2.5", className="progress-label", style={"fontSize": "1.35rem"}),
                dbc.Progress(
                    id="pm2.5-progress",
                    value=20,
                    max=100,
                    striped=True,
                    animated=True,
                    color="danger",
                    className="mb-3",
                ),
            ],
            className="progress-container",
        ),
        html.Div(
            [
                html.Div("PM 10", className="progress-label", style={"fontSize": "1.35rem"}),
                dbc.Progress(
                    id="pm10-progress",
                    value=10,
                    max=100,
                    striped=True,
                    animated=True,
                    color="warning",
                    className="mb-3",
                ),
            ],
            className="progress-container",
        ),
    ],
    className="post-box",
)

wd_bars = html.Div(
    [
        html.Div(
            [
                html.Div("Temperature", className="progress-label", style={"fontSize": "1.35rem"}),
                dbc.Progress(
                    id="temp-progress",
                    value=20,
                    max=100,
                    striped=True,
                    animated=True,
                    color="danger",
                    className="mb-3",
                ),
            ],
            className="progress-container",
        ),
        html.Div(
            [
                html.Div("Humidity", className="progress-label", style={"fontSize": "1.35rem"}),
                dbc.Progress(
                    id="rh-progress",
                    value=10,
                    max=100,
                    striped=True,
                    animated=True,
                    color="warning",
                    className="mb-3",
                ),
            ],
            className="progress-container",
        ),
        html.Div(
            [
                html.Div("Pressure", className="progress-label", style={"fontSize": "1.35rem"}),
                dbc.Progress(
                    id="press-progress",
                    value=10,
                    max=100,
                    striped=True,
                    animated=True,
                    color="warning",
                    className="mb-3",
                ),
            ],
            className="progress-container",
        ),
    ],
    className="post-box",
)

toast_descriptions = {
    "pollutants": """
            The main monitored gasses are Nitrogen oxides (NO2), Ozone (O3) and Carbon Oxide (CO).
            Nitrogen oxides are commonly produced by fuel combustion and a long term exposure to a high
            concentration of this gas can be dangerous. Carbon oxide is also produced by combustion but
            it is odorless and more toxic gas. Ozone is formed through a reaction with gases in presence
            of sunlight, so it is more common to find it during sunny days.
            """,
    "particulate_matter": """
            Particulate Matter, usually referred as PM followed by a number indicating the
            size of the particulate (e.g. PM10 and PM2.5), is a very common and meaningful
            indicator of air quality, as there is a strong evidence of negative health impact
            associated with the exposure of high concentration of PM. Usually PM are produced by
            combustion and its main components are sulfates, nitrates or black carbon, among others.
            """,
    "weather_data": """
            Temperature, Humidity and Pressure come
            from wheater stations. They are essential to understand
            patterns and correlations with changes in air quality.
            """,
}

descriptions = {
    "NO2": "Description for Nitrogen Dioxide",
    "O3": "Description for Ozone",
    "CO": "Description for Carbon Monoxide",
    "PM 2.5": "Description for Particulate Matter 2.5",
    "PM 10": "Description for Particulate Matter 10",
}

# Define the available pollutants for each location
available_pollutants = {
    "Trento - via Bolzano": ["NO2", "O3", "CO"],
    "Trento - S. Chiara": ["NO2", "O3", "PM 2.5", "PM 10", "SO2"],
}

# Define the dropdown for selecting the location
location_dropdown = dcc.Dropdown(
    options=[{"label": station, "value": station} for station in stations],
    id="location-dropdown",
    value="Trento - via Bolzano",
    className="dropdown",
)

# Define the buttons for selecting the pollutants
pollutant_buttons = html.Div(
    dbc.RadioItems(
        id="selected-fbk-pollutant",
        class_name="btn-group",
        input_class_name="btn-check",
        label_class_name="btn btn-outline-primary",
        label_checked_class_name="active",
        value="NO2",
    ),
    className="radio-group",
)


popup_menus = {
    "pollutants": dbc.Modal(
        [
            dbc.ModalHeader("Gas pollution", style={"fontSize": "4rem"}),
            dbc.ModalBody(toast_descriptions["pollutants"], style={"fontSize": "3rem"}),
            dbc.ModalFooter(
                dbc.Button(
                    "Close",
                    id="close-popup-no2",
                    className="ml-auto",
                    n_clicks=0,
                    style={"fontSize": "2.5rem"},
                )
            ),
        ],
        id="popup-menu-no2",
        size="lgs",
    ),
    "particulate_matter": dbc.Modal(
        [
            dbc.ModalHeader("Particulate matter", style={"fontSize": "4rem"}),
            dbc.ModalBody(
                toast_descriptions["particulate_matter"], style={"fontSize": "3rem"}
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "Close",
                    id="close-popup-o3",
                    className="ml-auto",
                    n_clicks=0,
                    style={"fontSize": "2.5rem"},
                )
            ),
        ],
        id="popup-menu-o3",
        size="lg",
    ),
    "weather_data": dbc.Modal(
        [
            dbc.ModalHeader("Weather data", style={"fontSize": "4rem"}),
            dbc.ModalBody(
                toast_descriptions["weather_data"], style={"fontSize": "3rem"}
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "Close",
                    id="close-popup-co",
                    className="ml-auto",
                    n_clicks=0,
                    style={"fontSize": "2.5rem"},
                )
            ),
        ],
        id="popup-menu-co",
        size="lg",
    ),
}

info_icons = {
    "pollutants": html.Div(
        [
            dbc.Tooltip(
                "Click for more info",
                target="info-icon-no2",
            ),
            html.I(
                className="fa-solid fa-info-circle",
                id="info-icon-no2",
                n_clicks=0,
                style={"cursor": "pointer"},
            ),
        ],
        className="info-icon-container",
    ),
    "particulate_matter": html.Div(
        [
            dbc.Tooltip(
                "Click for more info",
                target="info-icon-o3",
            ),
            html.I(
                className="fa-solid fa-info-circle",
                id="info-icon-o3",
                n_clicks=0,
                style={"cursor": "pointer"},
            ),
        ],
        className="info-icon-container",
    ),
    "weather_data": html.Div(
        [
            dbc.Tooltip(
                "Click for more info",
                target="info-icon-co",
            ),
            html.I(
                className="fa-solid fa-info-circle",
                id="info-icon-co",
                n_clicks=0,
                style={"cursor": "pointer"},
            ),
        ],
        className="info-icon-container",
    ),
}

toast_no2 = dbc.Toast(
    [pollutants_bars],
    id="pl_toast",
    header=[
        dbc.Row(
            [
                dbc.Col(
                    html.H4(
                        ["Gas Pollutants"],
                        className="section-header"
                    ),
                    width=11,
                ),
                dbc.Col(
                    html.H4(
                        [info_icons["pollutants"]],
                        className="section-header"
                    ),
                    width=1,
                ),
            ]
        )
    ],
    style={"height": "100%"},
)

toast_o3 = dbc.Toast(
    [pm_bars,],
    id="pm_toast",
    header=[
        dbc.Row(
            [
                dbc.Col(
                    html.H4(
                        ["Particulate Matter"],
                        className="section-header",
                    ),
                    width=11,
                ),
                dbc.Col(
                    html.H4(
                        [info_icons["particulate_matter"]],
                        className="section-header",
                    ),
                    width=1,
                ),
            ]
        ),
    ],
    style={"height": "100%"},
)

toast_co = dbc.Toast(
    [wd_bars,],
    id="wd_toast",
    header=[
        dbc.Row(
            [
                dbc.Col(
                    html.H4(
                        ["Weather Data"],
                        className="section-header",
                    ),
                    width=11,
                ),
                dbc.Col(
                    html.H4(
                        [info_icons["weather_data"]],
                        className="section-header",
                    ),
                    width=1,
                ),
            ]
        )
    ],
    style={"height": "100%"},
)


layout = html.Div(
    children=[
        html.Label(
            "Select location: ",
            style={"fontSize": "1.5rem"}
        ),
        dcc.Dropdown(
            options=[{"label": station, "value": station} for station in stations],
            id="location-dropdown",
            value="Trento - via Bolzano",
            className="dropdown",
            style={"maxWidth": "50rem"}
        ),
        gas_btns,
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            dbc.Row(
                                [toast_no2, html.Br()], className="vertical-spacing"
                            ),
                            dbc.Row(
                                [toast_o3, html.Br()], className="vertical-spacing"
                            ),
                            dbc.Row(
                                [toast_co, html.Br()], className="vertical-spacing"
                            ),
                        ],
                    ),
                    width=3,
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            id="pollutant-graph",
                            config={"displayModeBar": True},
                            className="pretty_container",
                            style={"margin": "4rem"},
                        ),
                        description_box,
                    ],
                    width=9,
                ),
            ],
            className="graph-container",
        ),
        popup_menus["pollutants"],
        popup_menus["particulate_matter"],
        popup_menus["weather_data"],
    ],
)


@callback(
    Output("popup-menu-no2", "is_open"),
    [Input("info-icon-no2", "n_clicks"), Input("close-popup-no2", "n_clicks")],
    [State("popup-menu-no2", "is_open")],
)
def toggle_popup_no2(n_clicks_open, n_clicks_close, is_open):
    if n_clicks_open or n_clicks_close:
        return not is_open
    return is_open


@callback(
    Output("popup-menu-o3", "is_open"),
    [Input("info-icon-o3", "n_clicks"), Input("close-popup-o3", "n_clicks")],
    [State("popup-menu-o3", "is_open")],
)
def toggle_popup_o3(n_clicks_open, n_clicks_close, is_open):
    if n_clicks_open or n_clicks_close:
        return not is_open
    return is_open


@callback(
    Output("description-box", "children"), [Input("selected-fbk-pollutant", "value")]
)
def update_description_box(selected_pollutant):
    return descriptions[selected_pollutant]

@callback(
    Output("selected-fbk-pollutant", "options"),
    [Input("location-dropdown", "value")]
)
def update_pollutant_buttons(selected_location):
    pollutants = available_pollutants.get(selected_location, [])
    options = [{"label": pollutant, "value": pollutant} for pollutant in pollutants]
    return options

@callback(
    Output("popup-menu-co", "is_open"),
    [Input("info-icon-co", "n_clicks"), Input("close-popup-co", "n_clicks")],
    [State("popup-menu-co", "is_open")],
)
def toggle_popup_co(n_clicks_open, n_clicks_close, is_open):
    if n_clicks_open or n_clicks_close:
        return not is_open
    return is_open


@callback(
    Output("pollutant-graph", "figure"),
    [Input("selected-fbk-pollutant", "value"), Input("location-dropdown", "value")],
)
def update_pollutant_graph(selected_pollutant, selected_location):
    # Generate some sample data
    station_df_key = station_labels_to_df_keys[selected_location]

    df_graph = df_s_p.loc[(station_df_key, selected_pollutant)]
    x = df_graph.ts
    y = df_graph.valore

    # Create a Plotly figure
    figure = go.Figure(data=go.Scatter(x=x, y=y, mode="lines+markers"))

    # Set the graph title and axes labels
    figure.update_layout(
        title=f"{selected_pollutant} Levels at {selected_location}",
        xaxis_title="Time",
        yaxis_title=f"{selected_pollutant} Levels",
        plot_bgcolor="white",
        paper_bgcolor="rgba(0,0,0,0)",
        legend={
            "bgcolor": "rgba(0,0,0,0)",
        },
        modebar=dict(bgcolor="#ffffff"),
    )
    figure.update_xaxes(
        title_font_size=12,
        showgrid=True,
        gridcolor="rgb(237, 232, 232)",
        gridwidth=0.5,
    )

    return figure
