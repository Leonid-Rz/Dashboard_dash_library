from dash import Dash, html, dcc, dash_table, callback, Output, Input
import plotly.express as px
import pandas as pd

from Parsing_data import df 


app = Dash(__name__)

app.layout = html.Div([
    html.Div(children='Выберете больницу'),
    html.Div([ 
        dcc.Checklist(            
            ['ГОБУЗ "Боровичская ЦРБ"','ГОБУЗ "Старорусская ЦРБ"', 'ГОБУЗ "НОКБ"'],
            ['ГОБУЗ "Боровичская ЦРБ"','ГОБУЗ "Старорусская ЦРБ"', 'ГОБУЗ "НОКБ"'], id='checkbox'), 
        html.Div(children='---'),
        dcc.Checklist(            
            ['Г','ГО', 'ГОБ'],
            ['Г','ГО', 'ГОБ'], id='heckbox'), 
        html.Div(children='Табличные данные'),
        dcc.RangeSlider(
                        min=1, max=12, 
                        step=1,
                        value=[1,12],
                        tooltip={"placement": "bottom", "always_visible": False},
                        vertical = True,
                        verticalHeight = 300,
                        id='my-slider'
                        ),
        html.Div(id='slider-output-container'),
        html.Div(id='datatable-container')
        ])
])


@callback(
    Output('datatable-container', 'children'),
    Input('checkbox', 'value'),
    Input('my-slider', 'value')
)
def update_datatable(selected_hospital, month):
    if not selected_hospital:
        return []
    new_df = df[df['Hospital'].isin(selected_hospital) & df['Month'].isin(range(month[0], month [1]))]
    return dash_table.DataTable(
        data=new_df.to_dict('records'), 
        page_size=50
)


if __name__ == '__main__':
    app.run(debug=True)
    


    new_df = df[df['Hospital'].isin('ГОБУЗ "Боровичская ЦРБ"')] & df[df['Month'].isin(8)]