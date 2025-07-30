# interface_dash/pages/visualisation.py
import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/visualisation", name="Visualisation des données")



layout = dbc.Container([
    html.H2("📊 Visualisation des données", className="mt-4"),
    
    dcc.Upload(
        id='upload-data-viz',
        children=html.Div([
            'Glissez un fichier ici ou ',
            html.A('sélectionnez un fichier')
        ]),
        style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed',
            'borderRadius': '5px', 'textAlign': 'center', 'margin-bottom': '20px'
        },
        multiple=False
    ),
    
    html.Div(id='data-preview'),
    html.Div(id='rul-histogram'),
    html.Div(id='unit-selection'),
    html.Div(id='sensor-curves')
])

@callback(
    Output('data-preview', 'children'),
    Output('rul-histogram', 'children'),
    Output('unit-selection', 'children'),
    Input('upload-data-viz', 'contents'),
    State('upload-data-viz', 'filename')
)
def update_output(contents, filename):
    if contents is None:
        return None, None, None

    content_type, content_string = contents.split(',')
    import base64, io
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    # Aperçu du dataframe
    preview = dbc.Table.from_dataframe(df.head(), striped=True, bordered=True, hover=True)

    # Histogramme RUL si la colonne existe
    hist = None
    if 'RUL' in df.columns:
        fig = px.histogram(df, x='RUL', nbins=50, title='Distribution du RUL')
        hist = dcc.Graph(figure=fig)

    # Dropdown unit
    unit_select = None
    if 'unit' in df.columns:
        unit_select = dcc.Dropdown(
            options=[{'label': str(i), 'value': i} for i in df['unit'].unique()],
            id='selected-unit',
            placeholder='Choisir un moteur (unit)',
            style={'marginTop': '20px'}
        )
        # Sauvegarde temporaire
        df.to_csv('data/temp/df_visualisation.csv', index=False)

    return preview, hist, unit_select

@callback(
    Output('sensor-curves', 'children'),
    Input('selected-unit', 'value')
)
def plot_sensors(unit_id):
    if unit_id is None:
        return None
    df = pd.read_csv('data/temp/df_visualisation.csv')
    df_unit = df[df['unit'] == unit_id]

    if 'cycle' not in df_unit.columns:
        return html.Div("Pas de colonne 'cycle' pour tracer les courbes")

    sensors = [col for col in df_unit.columns if 'sensor_' in col]

    graphs = []
    for sensor in sensors[:5]:  # limiter à 5 capteurs
        fig = px.line(df_unit, x='cycle', y=sensor, title=f"{sensor} - moteur {unit_id}")
        graphs.append(dcc.Graph(figure=fig))

    return graphs
