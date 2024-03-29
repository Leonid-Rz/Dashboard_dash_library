from dash import Dash, html, dcc

app = Dash(__name__)

# Создание бокового меню
sidebar = html.Nav(
    className='sidebar',
    children=[
        html.Ul(className='sidebar-nav',
            children=[
                html.Li(html.A('Главная', href='/')),
                html.Li(html.A('Страница 1', href='/page-1')),
                html.Li(html.A('Страница 2', href='/page-2')),
            ]
        )
    ]
)

# Создание макета приложения с боковым меню
app.layout = html.Div([
    sidebar,
    html.Div(id='page-content')
])

if __name__ == '__main__':
    app.run_server(debug=True)
