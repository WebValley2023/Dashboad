import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


# Sample data for demonstration
data = {
    'Location': ['Location 1', 'Location 2', 'Location 3'],
    'Gas Pollutant': [0.5, 0.8, 0.3],
    'Particulate Matter': [0.6, 0.4, 0.7],
    'Temperature': [25, 30, 28],
    'Pressure': [1012, 1015, 1008],
    'Humidity': [60, 65, 55],
    'Status': ['Saturated', 'Unsaturated', 'Saturated']
}
df = pd.DataFrame(data)


app = dash.Dash(__name__)


app.layout = html.Div(
    children=[
        html.Div(
            className='dropdown',
            children=[
                dcc.Dropdown(
                    id='location-dropdown',
                    options=[
                        {'label': 'Location 1', 'value': 'Location 1'},
                        {'label': 'Location 2', 'value': 'Location 2'},
                        {'label': 'Location 3', 'value': 'Location 3'}
                    ],
                    value='Location 1'
                )
            ]
        ),
        html.Div(
            className='heading',
            children=[
                html.H2('Total pollutant concentration')
            ]
        ),
        html.Div(
            className='bar-container',
            children=[
                html.Div(
                    className='bar',
                    children=[
                        html.Div(
                            className='bar-content',
                            children=[
                                html.P('0 ppm')
                            ]
                        ),
                        html.Div(
                            className='threshold yellow'
                        ),
                        html.Div(
                            className='threshold red'
                        ),
                        html.Div(
                            className='threshold purple'
                        ),
                        html.Div(
                            className='question-icon',
                            children=[
                                html.Span('?', id='question-mark')
                            ]
                        ),
                        html.Div(
                            className='popup',
                            children=[
                                dcc.Textarea(
                                    id='explanation-textarea',
                                    placeholder='Add explanation'
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        html.Div(
            className='box-container',
            children=[
                html.Div(
                    className='box',
                    children=[
                        html.H3('Gas pollutants'),
                        html.Div(
                            className='question-icon',
                            children=[
                                html.Span('?', id='gas-question-mark')
                            ]
                        ),
                        html.Div(
                            'O3',
                            className='sensor-info'
                        ),
                        html.Div(
                            className='bar',
                            children=[
                                html.Div(
                                    className='bar-content',
                                    children=[
                                        html.P('0 ppm', id='o3-concentration')
                                    ]
                                ),
                                html.Div(
                                    className='threshold yellow'
                                ),
                                html.Div(
                                    className='threshold red'
                                ),
                                html.Div(
                                    className='threshold purple'
                                )
                            ]
                        ),
                        html.Div(
                            'NO2',
                            className='sensor-info'
                        ),
                        html.Div(
                            className='bar',
                            children=[
                                html.Div(
                                    className='bar-content',
                                    children=[
                                        html.P('0 ppm', id='no2-concentration')
                                    ]
                                ),
                                html.Div(
                                    className='threshold yellow'
                                ),
                                html.Div(
                                    className='threshold red'
                                ),
                                html.Div(
                                    className='threshold purple'
                                )
                            ]
                        ),
                        html.Div(
                            'Third Pollutant',
                            className='sensor-info'
                        ),
                        html.Div(
                            className='bar',
                            children=[
                                html.Div(
                                    className='bar-content',
                                    children=[
                                        html.P('0 ppm', id='third-pollutant-concentration')
                                    ]
                                ),
                                html.Div(
                                    className='threshold yellow'
                                ),
                                html.Div(
                                    className='threshold red'
                                ),
                                html.Div(
                                    className='threshold purple'
                                )
                            ]
                        ),
                    ]
                ),
                html.Div(
                    className='box',
                    children=[
                        html.H3('Particulate Matter'),
                        html.Div(
                            className='question-icon',
                            children=[
                                html.Span('?', id='pm-question-mark')
                            ]
                        ),
                        html.Div(
                            'PM2.5',
                            className='sensor-info'
                        ),
                        html.Div(
                            className='bar',
                            children=[
                                html.Div(
                                    className='bar-content',
                                    children=[
                                        html.P('0 µg/m³', id='pm-concentration')
                                    ]
                                ),
                                html.Div(
                                    className='threshold yellow'
                                ),
                                html.Div(
                                    className='threshold red'
                                ),
                                html.Div(
                                    className='threshold purple'
                                )
                            ]
                        ),
                    ]
                )
            ]
        ),
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)


