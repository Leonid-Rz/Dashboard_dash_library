from dash import Dash, html, dcc, dash_table, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_html_components as html

from Parsing_data import df 
from Filters import choosing_a_hospital, choosing_a_year, choosing_the_month, table

app = Dash(__name__)

app.layout =  html.Div( children= [
                        choosing_a_hospital,
                        choosing_a_year, 
                        choosing_the_month, 
                        table
])


@callback(
    Output('datatable-container', 'children'),
    Input('choose_a_hospital', 'value'),
    Input('monthly_slider', 'value'),
    Input('choose_a_year', 'value')
)
def update_datatable(selected_hospital, month, year):
    if not selected_hospital or not year:
        return []
    t_year=[int (x) for x in year]
    new_df = df[(df['Hospital'].isin(selected_hospital)) & (df['Month'].isin(range(month[0], month [1]+1))) & (df['Date'].dt.year.isin (t_year))]
    return dash_table.DataTable(
        style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
    },
        data=new_df.to_dict('records'), 
        page_size=30
)


if __name__ == '__main__':
    app.run(debug=True)