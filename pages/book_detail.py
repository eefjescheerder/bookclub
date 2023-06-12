import dash
from dash import html
from getData import getData
import dash_bootstrap_components as dbc
import html as htmlParser


data = getData()
booksdf = data['booksdf']
sumdf = data['sumdf']


def generate_tooltip(text, id):
    return html.Div(
        [
            html.Span(
                "?",
                id="tooltip-target-"+str(id),
                style={
                        "textAlign": "center", 
                        "color": "pink"
                },
                className="dot"),

            dbc.Tooltip(
                text,
                target="tooltip-target-"+str(id),
            )
        ], 
        style={
            "position": "absolute", 
            "top": "4px",
            "right": "15px"
        }
    )

dash.register_page(
    __name__,
    path_template="/book-gallery/<isbn>",
    title='Book Detail',
    name='Book Detail',
    nav_exlcude=True
)


def layout(isbn=None):
    if isbn == None:
        return
    
    book = booksdf.loc[booksdf["isbn"] == isbn]
    snippet = htmlParser.unescape(book.iloc[0][15])
    summary = sumdf.loc[sumdf["isbn"] == isbn]
    summary = htmlParser.unescape(summary.iloc[0][3])
    wordcloud = str("/assets/" +book.iloc[0][3] + ".png")
    
    return dbc.Container([
        dbc.Row([
            dbc.Card(
                dbc.CardBody(html.H1(book.iloc[0][3])),
                style={"text-align":"center", "background-color": 'rgba(0,0,0,0)'}
            ),
            dbc.Card(
                dbc.CardBody([
                    generate_tooltip("Book snippet from Google", "snippet"),
                    dbc.CardBody(snippet)
                ])  
            ),
            dbc.Card(
                dbc.CardBody([
                    #Summary
                    generate_tooltip("This is a computer generated summary based on all Goodreads reviews. The scraped reviews have been translated into English first.", "summary"),
                    dbc.CardBody(summary)
                ])  
            ),
            dbc.Card(
                dbc.CardBody([
                    generate_tooltip("This wordcloud is based on all Goodread reviews.", "wordcloud"),
                    dbc.CardImg(src=wordcloud, style={ "max-width": "150%" })
                ])  
            )
        ])
    ])
