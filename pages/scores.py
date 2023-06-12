import dash
import plotly.express as ps
from dash import html, dcc, Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from getData import getData, getOverallAveragePerMember, getOverallAveragesPerBook
import plotly.express as px


dash.register_page(
    __name__,
    path='/scores',
    title='Scores',
    name='Scores'
)

def generate_tooltip(text, id):
    return html.Div(
        [
            html.Span(
                "?",
                id="tooltip-target-"+str(id),
                style={
                        "textAlign": "center", 
                        "color": "lightsalmon"
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


data = getData()
overallAveragePerMember = getOverallAveragePerMember(data["scoresdf"])
overallAveragePerBook = getOverallAveragesPerBook(data["scoresdf"])
scoresdf = data["scoresdf"]
booksdf = data['booksdf']

# get current amount of books 
groupDf = scoresdf.groupby(['book']).mean().reset_index()
count = len(groupDf)


cards = dbc.CardGroup(
    [
            dbc.Card(
                dbc.CardBody(
                    [
                        generate_tooltip("This represents the member that gave the lowest scores on all books on all categories on average", "cardNegMember"),
                        html.H4("Most negative member is"),
                        html.H1(overallAveragePerMember.keys()[0])
                    ]
                )
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        generate_tooltip("This represents the member that gave the lowest scores on all books on all categories on average.", "cardPosMember"),
                        html.H4("Most Positive member is"),
                        html.H1(overallAveragePerMember.keys()[-1:])
                    ]
                )
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        generate_tooltip("This represents the book that got the highest overall score.", "cardFavBook"),
                        html.H4("Our all time favourite book is"),
                        html.H1(overallAveragePerBook['book'][-1:]),
                        html.H4("by"),
                        html.H2(data['booksdf'].loc[data['booksdf']['title'] == overallAveragePerBook['book'].iloc[-1]]['author'])
                    ]
                )
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        generate_tooltip("This represents the book that got the lowest overall score.", "cardLeastFavBook"),
                        html.H4("Our all time least favourite book is"),
                        html.H1(overallAveragePerBook['book'][0]),
                        html.H4("by"),
                        html.H2(data['booksdf'].loc[data['booksdf']['title'] == overallAveragePerBook['book'][0]]['author'])
                    ]
                )
            )
    ]
)

def createBookScoreChart(chartDf, x, title):
    barCount = len(chartDf)
    fig = px.bar(chartDf, x=x, y='book', color_discrete_sequence=px.colors.diverging.Spectral[:barCount], color="book")
    fig.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'
    })
    fig.update_layout(showlegend=False) 
    fig.update_layout(
        title={
            'text': title,
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig.update_layout(
        xaxis_title=" ",
        yaxis_title=" ",
        font=dict(
            color="white"
        )
    )
    return fig   

avgPerBookFig = createBookScoreChart(overallAveragePerBook, 'overall', "Overall")
plotFig = createBookScoreChart(scoresdf.groupby(['book']).mean().reset_index(), "plot", "Plot")
thinkFig = createBookScoreChart(scoresdf.groupby(['book']).mean().reset_index(), "madeyouthink", "Made you think")
styleFig = createBookScoreChart(scoresdf.groupby(['book']).mean().reset_index(), "writingstyle", "Writing style")
readFig = createBookScoreChart(scoresdf.groupby(['book']).mean().reset_index(), "readability", "Readability")

mergedDf = scoresdf.merge(booksdf, left_on=['book'], right_on='title')
mergedDf = mergedDf[['member', 'book', 'overall', 'goodreads_rating']].copy()
mergedDf['diff'] = mergedDf['goodreads_rating'] - mergedDf['overall']
mergedDf['diff'] = mergedDf['diff'].abs()

goodreadsDifFig = createBookScoreChart(mergedDf.groupby(['book']).mean().reset_index(), "diff", "Difference between our scores and Goodreads")

# Recommendation Pie Chart
scoresdf['recommend'] = scoresdf['recommend'].apply(str.upper)
recList = scoresdf["recommend"].value_counts().index.tolist()
recCount = scoresdf['recommend'].value_counts()
recCountList = recCount.tolist()

# Change F to Female, M to Male in list
for i in range(len(recList)):
 
    if recList[i] == 'N':
        recList[i] = 'We would not recommend :('
        
    if recList[i] == 'Y':
        recList[i] = 'We would recommend :)'
        
        
recPie = go.Figure(data=[go.Pie(labels=recList,
                             values=recCountList)])
recPie.update_traces(hoverinfo='label+percent', textinfo='label', textfont_size=12,
                  marker=dict(colors=px.colors.diverging.Spectral, line=dict(color='#000000', width=2)))
recPie.update(layout_showlegend=False)
recPie.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'
})
recPie.update_layout(
    title={
        'text': "How often do we recommend a book?",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
recPie.update_layout(font=dict(color="white"))

# Finish book pie chart
scoresdf['finish'] = scoresdf['finish'].apply(str.upper)
finList = scoresdf["finish"].value_counts().index.tolist()
finCount = scoresdf['finish'].value_counts()
finCountList = finCount.tolist()

# Change F to Female, M to Male in list
for i in range(len(finList)):
 
    if finList[i] == 'N':
        finList[i] = "We wouldn't have finished it :()"
        
    if finList[i] == 'Y':
        finList[i] = 'We would finish it :)'
        
finPie = go.Figure(data=[go.Pie(labels=finList,
                             values=finCountList)])
finPie.update_traces(hoverinfo='label+percent', textinfo='label', textfont_size=12,
                  marker=dict(colors=px.colors.diverging.Spectral, line=dict(color='#000000', width=2)))
finPie.update(layout_showlegend=False)
finPie.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'
})
finPie.update_layout(
    title={
        'text': "How often would we have finished the book, <br> if it wasn't for the book club?",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
finPie.update_layout(font=dict(color="white"))


layout = dbc.Container([
        
    dbc.Row([
        cards 
    ]),
    
    dbc.Row([
        
        dbc.Col([
            
            html.Div(
            children=[
                html.Div(children = 'Select a member', style={'fontSize': "24px"},className = 'menu-title'),
                dcc.Dropdown(
                    id = 'member-filter',
                    options = [
                        {'label': Member, 'value':Member} 
                        for Member in scoresdf.member.unique()
                    ], #'Year' is the filter
                    value ='All',
                    clearable = True,
                    searchable = False,
                    className = 'dropdown', style={'fontSize': "24px",'textAlign': 'center'},
                ),
            ],
            className = 'menu',
            ), #the dropdown function
            
        ]),
        
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                figure=avgPerBookFig,
                id = "avgPerBookFig"
            )], width=6),
        
            dbc.Col([
                dcc.Graph(
                    figure=goodreadsDifFig,
                    id = "goodreadsDifFig"
                )], width=6),
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                figure=plotFig,
                id = 'plotFig'
            )], width=6),
        
            dbc.Col([
                dcc.Graph(
                    figure=thinkFig,
                    id = "thinkFig"
                )], width=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                figure=readFig,
                id = "readFig"
            )
        ]),
        dbc.Col([
            dcc.Graph(
                figure=styleFig,
                id = "styleFig"
            )
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                figure=recPie,
                id = "recPie"
            )
        ], width=6),
        dbc.Col([
            dcc.Graph(
                figure=finPie,
                id = "finPie"
            )
        ], width=6)
    ]),
    
])

@callback(
    Output("avgPerBookFig", "figure"),
    [Input("member-filter", "value")]
)
def update_charts(Member):
    if not Member:
        return createBookScoreChart(overallAveragePerBook, 'overall', "Overall")
    else:
        filtered_data = scoresdf[scoresdf["member"] == Member]
        return createBookScoreChart(filtered_data.groupby(['book']).mean().reset_index(), "overall", "Overall")

@callback(
    Output("goodreadsDifFig", "figure"),
    [Input("member-filter", "value")]
)
def update_charts(Member):
    if not Member:
        return createBookScoreChart(mergedDf.groupby(['book']).mean().reset_index(), "diff", "Difference between our score and Goodreads")
    else:
        filtered_data = mergedDf[mergedDf["member"] == Member]
        return createBookScoreChart(filtered_data.groupby(['book']).mean().reset_index(), "diff", "Difference between our score and Goodreads")
    
 
@callback(
    Output("plotFig", "figure"),
    [Input("member-filter", "value")]
)
def update_charts(Member):
    if not Member:
        return createBookScoreChart(scoresdf.groupby(['book']).mean().reset_index(), "plot", "Plot")
    else:
        filtered_data = scoresdf[scoresdf["member"] == Member]
        return createBookScoreChart(filtered_data.groupby(['book']).mean().reset_index(), "plot", "Plot")
 
    

@callback(
    Output("thinkFig", "figure"),
    [Input("member-filter", "value")]
)
def update_charts(Member):
    if not Member:
        return createBookScoreChart(scoresdf.groupby(['book']).mean().reset_index(), "madeyouthink", "Made you think")
    else:
        filtered_data = scoresdf[scoresdf["member"] == Member]
        return createBookScoreChart(filtered_data.groupby(['book']).mean().reset_index(), "madeyouthink", "Made you think")
 
@callback(
    Output("styleFig", "figure"),
    [Input("member-filter", "value")]
)
def update_charts(Member):
    if not Member:
        return createBookScoreChart(scoresdf.groupby(['book']).mean().reset_index(), "writingstyle", "Writing style")
    else:
        filtered_data = scoresdf[scoresdf["member"] == Member]
        return createBookScoreChart(filtered_data.groupby(['book']).mean().reset_index(), "writingstyle", "Writing style")
 
@callback(
    Output("readFig", "figure"),
    [Input("member-filter", "value")]
)
def update_charts(Member):
    if not Member:
        return createBookScoreChart(scoresdf.groupby(['book']).mean().reset_index(), "readability", "Readability")
    else:
        filtered_data = scoresdf[scoresdf["member"] == Member]
        return createBookScoreChart(filtered_data.groupby(['book']).mean().reset_index(), "readability", "Readability")

    
@callback(
    Output("finPie", "figure"),
    [Input("member-filter", "value")]
)
def update_charts(Member):
    finishTemplate = "%s would have finished it"
    notFinishTemplate = "%s wouldn't have finished it"
    finPieData = False
    
    if not Member:
        finPieData = scoresdf 
        name = "we"
    else:
        finPieData = scoresdf[scoresdf["member"] == Member]
        name = Member

    finPieData['finish'] = finPieData['finish'].apply(str.upper)
    finList = finPieData["finish"].value_counts().index.tolist()
    finCount = finPieData['finish'].value_counts()
    finCountList = finCount.tolist()

    # Change F to Female, M to Male in list
    for i in range(len(finList)):
    
        if finList[i] == 'N':
            finList[i] = notFinishTemplate % (name.capitalize())
            
        if finList[i] == 'Y':
            finList[i] = finishTemplate % (name.capitalize())
            

    finPie.update(data=[go.Pie(labels=finList, values=finCountList)])
    finPie.update_layout(
        title_text="How often would %s have finished the book, <br> if it wasn't for the book club?" % name)
    return finPie


@callback(
    Output("recPie", "figure"),
    [Input("member-filter", "value")]
)
def update_rec_pie_charts(Member):
    finishTemplate = "%s would recommend a book"
    notFinishTemplate = "%s would not recommend a boek"
    recPieData = False

    if not Member:
        recPieData = scoresdf 
        name = "we"
        titletext = "How often do %s recommend a book?"
    else:
        recPieData = scoresdf[scoresdf["member"] == Member]
        name = Member
        titletext = "How often does %s recommend a book?" 
    
    # Recommendation Pie Chart  
    recPieData['recommend'] = recPieData['recommend'].apply(str.upper)
    recList = recPieData["recommend"].value_counts().index.tolist()
    recCount = recPieData['recommend'].value_counts()
    recCountList = recCount.tolist()

    # Change F to Female, M to Male in list
    for i in range(len(recList)):
    
        if recList[i] == 'N':
            recList[i] = notFinishTemplate % (name.capitalize())
            
        if recList[i] == 'Y':
            recList[i] = finishTemplate % (name.capitalize())
            
    recPie.update(data=[go.Pie(labels=recList, values=recCountList)])
    recPie.update_layout(title_text=titletext % name)

    return recPie
