from dash import Dash, html, callback, Output, Input, State
import dash_bootstrap_components as dbc
import flask
import dash_auth

from Dashboard.Calculations import #choose_hospital_ASC
from Dashboard.Filters import #sidebar
from Dashboard.Content import #content


app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'], 'Montréal')
])

if __name__ == '__main__':
    app.run(debug=True)