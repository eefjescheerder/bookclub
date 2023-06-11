import dash
from dash import html
from getData import getData
import dash_bootstrap_components as dbc

data = getData()
booksdf = data['booksdf']
scoresdf = data['scoresdf']

# Y/N values to uppercase 
scoresdf['recommend'] = scoresdf['recommend'].apply(str.upper)

# Check for books where everyone voted YES on 'Recommend' 
booklistSame = []
booklist = (scoresdf.book.unique())
for book in booklist:
    tempDf = scoresdf.loc[scoresdf['book'] == book]
    if (tempDf['recommend'] == 'N').all():
        booklistSame.append(book)

# Create new df based on booklistSame 
filter = booksdf["title"].isin(booklistSame)
booksdfFilt = booksdf[filter]
booksdfFilt.drop_duplicates(subset=['title'])

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
    path='/wall-of-shame',
    title='Wall of Shame',
    name='Wall of Shame'
)

images = []
for index, row in booksdfFilt.iterrows():
    images.append(generate_image(row))

layout = dbc.Container([
    html.Div(
        [
            html.Span(
                html.H1("?"), 
                id="quest-mark"         
                    ),
                    dbc.Tooltip(
                    "This page shows all of the books that none of us would recommend. Click on a books image for more information about the book.",
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
