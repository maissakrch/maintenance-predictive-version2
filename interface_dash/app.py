import dash
import pages.visualisation  # en haut avec les autres

from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_pages.predict as predict_page

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/predict':
        return predict_page.layout()
    else:
        return html.Div([html.H1("Bienvenue sur le Dashboard Maintenance")])

if __name__ == '__main__':
    app.run(debug=True)
