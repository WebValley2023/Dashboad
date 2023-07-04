import os
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import dash

pd.options.mode.chained_assignment = None  # default='warn'


app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
)

sidebar = html.Div(
    [
        html.Div(
            [
                html.Img(src="/assets/img/logo_cut.png", style={"width": "5rem"}),
                html.H2("Airwatching"),
            ],
            className="sidebar-header",
        ),
        html.Hr(className="sidebar-hr"),
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-square-poll-vertical fa-2x"),
                        html.Br(),
                        html.Span("Raw FBK Data"),
                    ],
                    href="/",
                    id="raw-data-link",
                    active="exact",
                    style={"text-align": "center"},
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-chart-line fa-2x"),
                        html.Br(),
                        html.Span("Fitted FBK Data"),
                    ],
                    href="/fbk",
                    id="fitted-data-link",
                    active="exact",
                    style={"text-align": "center"},
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-smog fa-2x"),
                        html.Br(),
                        html.Span("APPA Data"),
                    ],
                    href="/appa",
                    id="appa-data-link",
                    active="exact",
                    style={"text-align": "center"},
                ),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(className="sidebar-hr"),
        html.Div(
            html.Img(src="/assets/img/fbk-logo.png", className="fbk-logo"),
            className="fbk-logo-div",
        ),
    ],
    className="sidebar",
)

popup_menu = dbc.Modal(
    [
        dbc.ModalHeader("Select Role"),
        dbc.ModalBody(
            [
                dbc.Button(
                    "User",
                    color="primary",
                    className="mr-3",
                    id="user-button",
                    n_clicks=0,
                ),
                dbc.Button(
                    "Researcher",
                    color="primary",
                    className="mr-3",
                    id="researcher-button",
                    n_clicks=0,
                ),
                html.Div(id="popup-content"),
            ]
        ),
    ],
    id="popup",
    is_open=True,
    centered=True,
    backdrop="static",
    style={"background-color": "rgba(0, 0, 0, 0.4)"},
)

content = html.Div(
    [
        dcc.Location(id="url"),
        sidebar,
        html.Div(id="page-content", className="content"),
        popup_menu,
    ]
)

app.layout = html.Div([content, html.Div(id="background")])
server = app.server


@app.callback(
    Output("popup-content", "children"),
    [Input("user-button", "n_clicks"), Input("researcher-button", "n_clicks")],
)
def update_popup_content(user_clicks, researcher_clicks):
    if user_clicks > 0:
        return html.Div("User selected")
    elif researcher_clicks > 0:
        return html.Div("Researcher selected")
    else:
        return ""


@app.callback(
    Output("popup", "is_open"),
    Output("background", "style"),
    Output("page-content", "children"),
    [Input("researcher-button", "n_clicks")],
)
def close_popup(researcher_clicks):
    if researcher_clicks > 0:
        return (
            False,
            {"display": "none"},
            html.Div(
                [
                    html.H1("Raw FBK Data"),
                    # Add your content specific to the "Raw FBK Data" page here
                    # For example, you can include dash components, tables, etc.
                ]
            ),
        )
    return True, {"background-color": "rgba(0, 0, 0, 0.4)"}, ""


@app.callback(
    [
        Output("raw-data-link", "active"),
        Output("fitted-data-link", "active"),
        Output("appa-data-link", "active"),
    ],
    [Input("url", "pathname")],
)
def update_active_links(pathname):
    return pathname == "/", pathname == "/fbk", pathname == "/appa"


if __name__ == "__main__":
    if os.getenv("DEBUG"):
        app.run(debug=True)
    else:
        # Production
        app.run_server(port=8033, host="0.0.0.0", debug=True)
