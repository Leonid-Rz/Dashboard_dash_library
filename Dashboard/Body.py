from dash import Dash, html, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_html_components as html

from Blocks import head, sidebar_and_cards, table_block
from Calculation import calculations, table_and_button

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children= [
                            head,
                            sidebar_and_cards,
                            table_block
                            ], className='big_color'
                            )

@callback(
    Output('total_ASC', 'children'),
    Output('ACS_with_ST', 'children'),
    Output('ACS_without_ST', 'children'),
    Output('PCI_coverage', 'children'),
    Output('ACS_mort_rate', 'children'),
    Output('MI_mortality_rate', 'children'),
    Output('ACS-hist', 'figure'),
    Output('ACS_way', 'figure'),
    Output('ACS_with_eST_risk', 'figure'),
    Input('choose_a_hospital', 'value'),
    Input('monthly_slider', 'value'),
    Input('choose_a_year', 'value')
)
def intermediate_function (*args):
    return calculations (*args)

@callback(
    Output('datatable-container', 'children'),
    Input('choose_a_hospital', 'value'),
    Input('monthly_slider', 'value'),
    Input('choose_a_year', 'value'),
    Input('show-table-button', 'n_clicks')
)
def intermediate_function_2 (*args, **kwargs):
    return table_and_button (*args, **kwargs)

if __name__ == '__main__':
    app.run(debug=True)