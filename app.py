from dotenv import load_dotenv
load_dotenv()

import os

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SOLAR])


nav_pages = filter(lambda x: "nav_exlcude" not in x or x["nav_exlcude"] == False, dash.page_registry.values())


app.layout= html.Div(
    [
        html.H1("Book club"),
        html.Div([
            dcc.Link(page['name']+"  |  ", href=page['path'], style={"color": "lightyellow"})
            for page in nav_pages
        ]),
        html.Hr(),

        # content of each page
        dash.page_container
    ]
)


if __name__ == "__main__":
    app.run(debug=False)
