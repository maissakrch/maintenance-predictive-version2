import dash
from dash import dcc, html, Input, Output, State, callback
import requests
import pandas as pd
import io

dash.register_page(__name__, path="/predict", name="Prédiction")

layout = html.Div([
    html.H2("📊 Prédiction de la durée de vie restante (RUL)"),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Glissez un fichier CSV ici ou ', html.A('cliquez pour le sélectionner')]),
        style={
            'width': '100%',
            'height': '100px',
            'lineHeight': '100px',
            'borderWidth': '2px',
            'borderStyle': 'dashed',
            'borderRadius': '10px',
            'textAlign': 'center',
            'margin': '20px'
        },
        multiple=False
    ),
    html.Div(id='prediction-result', style={'marginTop': 20})
])

@callback(
    Output('prediction-result', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(contents, filename):
    if contents is None:
        return ""
    
    import base64
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    files = {'file': (filename, io.BytesIO(decoded), 'text/csv')}

    try:
        response = requests.post("http://127.0.0.1:5000/predict", files=files)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
            return html.Div([
                html.P("✅ Fichier traité avec succès. Voici les premières lignes avec la prédiction :"),
                dcc.Graph(figure={
                    'data': [{
                        'x': df.index,
                        'y': df["predicted_RUL"],
                        'type': 'line',
                        'name': 'RUL prédite'
                    }],
                    'layout': {
                        'title': 'RUL prédite par moteur',
                        'xaxis': {'title': 'Index'},
                        'yaxis': {'title': 'Durée de vie restante (RUL)'}
                    }
                })
            ])
        else:
            return html.Pre(response.text, style={'color': 'red'})
    except Exception as e:
        return html.Pre(str(e), style={'color': 'red'})
