from dash import Dash, html, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_html_components as html

from Blocks import head, sidebar_and_cards, table_block
from Calculation import calculations

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
    Output('datatable-container', 'children'),
    Input('choose_a_hospital', 'value'),
    Input('monthly_slider', 'value'),
    Input('choose_a_year', 'value'),
    Input('show-table-button', 'n_clicks')
)
def intermediate_function (*args, **kwargs):
    return calculations (*args, **kwargs)


if __name__ == '__main__':
    app.run(debug=True)

