import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
from getData import getBooks, getData
import datetime 

data = getData()
booksdf = data["booksdf"]
bookList = getBooks(booksdf)

daysLeft = str((booksdf["end_date"].iloc[-1] - datetime.datetime.now()).days)
booksRead = str(len(bookList)-1)
pagesRead = sum(booksdf['pages']) - booksdf['pages'].iloc[-1]
daysReading = (booksdf["start_date"].iloc[-1] - booksdf["start_date"].iloc[0]).days
avgPagesPerDay = str(round(pagesRead / daysReading))
avgPagesPerWeek = str(round(pagesRead / daysReading * 7))
avgPagesPerMonth = str(round(pagesRead / daysReading * 365 / 12))
avgPagesPerYear = str(round(pagesRead / daysReading * 365))

dash.register_page(__name__, path='/')






layout = html.Div(
    [
    html.A(
        href="./book-gallery",
        children=[
            html.Img(
                alt= bookList[-1],
                src=booksdf["images"].iloc[-1],
                style={
                    'height': '18%',
                    'width': '18%'
                })
        ]
    ),

    html.H2(),
    html.H3(
        "We are currently reading: "),
    html.H1(bookList[-1] + " by " + booksdf["author"].iloc[-1] + "."
    ),
    html.H4(
        "We have " + daysLeft + " days left to finish the book."
    ),
    html.H4(
        "So far, we have read " + booksRead + " books and " + str(pagesRead) + " pages." 
    ),
    html.H6(
        "This means that on average, we read "),
    html.Div(id='analytics-output', style={ "display": "inline-block", "font-size":"20px" }),
    html.Div([
        dcc.Dropdown(
            ['Day', 'Week','Month', 'Year'],
            'Day',
            id='analytics-input',
            className="btn-sm",
            clearable=False,
            style={ "height": "28px" }
        )
        ], 
        style={ "width": "10%", "Align":"center", "display": "inline-block" }
    ),
     html.Br(
         )
    
    
    ], style={'textAlign': 'center'}
)


@callback(
    Output(component_id='analytics-output', component_property='children'),
    Input(component_id='analytics-input', component_property='value')
)
def update_city_selected(input_value):
    if input_value == "Day":
        pages = avgPagesPerDay
    elif input_value == "Week":
        pages = avgPagesPerWeek
    elif input_value == "Month":
        pages = avgPagesPerMonth
    else: 
        pages = avgPagesPerYear
    return f'{pages} pages per '