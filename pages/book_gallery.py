import dash
from dash import html
from getData import getData
import dash_bootstrap_components as dbc


data = getData()
booksdf = data['booksdf']

def generate_image(book):

    return html.A(
                href="./book-gallery/%s" % (book['isbn']),
                style={
                    'width': '32%',
                    'display': 'inline-block'
                },
                children=[
                    html.Img(
                        src=book["images"],
                        style={
                            'width': '200px',
                            'display': 'block',
                            'margin': 'auto'
                        }
                    )
                ]
            )
 
def generate_image(book):

    return html.A(
                href="./book-gallery/%s" % (book['isbn']),
                style={
                    'width': '32%',
                    'display': 'inline-block'
                },
                children=[
                    
                    html.Img(
                        src=book["images"],
                        style={
                            'width': '200px',
                            'display': 'block',
                            'margin': 'auto'
                        }
                    )
                ]
            )
       


dash.register_page(
    __name__,
    path='/book-gallery',
    title='Gallery',
    name='Gallery'
)

images = []
for index, row in booksdf.iterrows():
    images.append(generate_image(row))

layout = dbc.Container([
    html.Div(
        [
            html.Span(
                html.H1("?"), 
                id="quest-mark"         
                    ),
                    dbc.Tooltip(
                    """Click on a cover to see more information about the book.""",
                    target="quest-mark"
            ),
 
        ],
        style={
            "position": "absolute", 
            "top": "100px",
            "right": "15px"
        }   
    ),
    html.Div(
    className="card-columns",
    children=images,
    style= {
        'margin-left': 'auto',
        'margin-right': 'auto'
    }
        
        
),
])

