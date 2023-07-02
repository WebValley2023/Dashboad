from dash import Dash, Input, Output, html, State, dcc
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Testing"

df = pd.read_csv('/plotly-app/pages/map.json')

modal = html.Div(
    [
        dbc.Button("Open modal", id="open", n_clicks=0, className=".btn"),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Click a point to see the data"), className="modal-header"),
                dbc.ModalBody(dcc.Graph(id='figure')),
            ],
            id="modal-map",
            is_open=True,
            centered=True,
            size="lg",
        ),
    ]
)

app.layout = html.Div(
    [
        modal,
    ]
)


@app.callback(
    Output("modal-map", "is_open"),
    Input("open", "n_clicks"),
    State("modal-map", "is_open")
)
def toggle_modal(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open


@app.callback(
    Output("figure", "figure"),
    Input("modal-map", "is_open")
)
def update_graph(is_open):
    if is_open:
        italy_geojson = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/italy_regions.geojson'

        fig = go.Figure()

        fig.add_trace(go.Scattermapbox(
            mode='markers',
            lon=[11.11022, 11.1262],  # Longitude of the specific places
            lat=[46.10433, 46.06292],  # Latitude of the specific places
            marker=dict(
                size=[16, 20],  # Size of the dots
                color='green',    # Color of the dots
                opacity=1,      # Make the dots fully visible
            ),
            text=['Via Bolzano', 'S.Chiaro'],  # Text to display on the dots
            hoverinfo='text',  # Remove hover information
             hoverlabel=dict(
                font=dict(
                    size=20  # Set the font size of the hover text
                )
            )
            
        ))
        
        

        fig.update_layout(
            title_text='',
            mapbox_style='carto-positron',
            mapbox_zoom=9,
            mapbox_center={"lat": 46.069425, "lon": 11.13568},
            width=1000,
            height=800,
            mapbox=dict(
                layers=[
                    dict(
                        sourcetype='geojson',
                        source=italy_geojson,
                        type='fill',
                        color='rgba(0,0,0,0)'
                    )
                ]
            )
        )

        return fig

    return go.Figure()


if __name__ == "__main__":
    app.run_server(debug=True)
