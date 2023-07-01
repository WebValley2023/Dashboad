from dash import Dash, Input, Output, html, State, dcc
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Playground!"

df = pd.read_csv('/home/wvuser/webvalley-dashboard/plotly-app/map.json')

modal = html.Div(
    [
        dbc.Button("Open modal", id="open", n_clicks=0, className=".btn"),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Header")),
                dbc.ModalBody(dcc.Graph(id='figure')),
            ],
            id="modal",
            is_open=True,
            centered=True,
            style={"width": "1500px", "height": "1500px", "position": "fixed", "top": "50%", "left": "50%", "transform": "translate(-50%, -50%)"}
        ),
    ]
)

app.layout = html.Div(
    [
        modal,
    ]
)


@app.callback(
    Output("modal", "is_open"),
    Input("open", "n_clicks"),
    State("modal", "is_open")
)
def toggle_modal(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open


@app.callback(
    Output("figure", "figure"),
    Input("modal", "is_open")
)
def update_graph(is_open):
    if is_open:
        italy_geojson = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/italy_regions.geojson'

        fig = go.Figure(go.Choroplethmapbox(
            geojson=italy_geojson,
            locations=[],
            z=[],
            colorscale='Viridis',
            zmin=0,
            zmax=1
        ))

        fig.update_layout(
            title_text='',
            mapbox_style='carto-positron',
            mapbox_zoom=7,
            mapbox_center={"lat": 41.8719, "lon": 12.5675},
            width=1000,
            height=800
        )

        return fig

    return go.Figure()


if __name__ == "__main__":
    app.run_server(debug=True)
