import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from getData import getData, getBooks
import pycountry 
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
import base64

dash.register_page(
    __name__,
    path='/book-statistics',
    title='Statistics',
    name='Statistics'
)

data = getData()
booksdf = data["booksdf"]
scoresdf = data["scoresdf"]
bookList = getBooks(booksdf)

fontDict = dict(
        family="monospace",
        size=14,
        color="white"
    )


genderList = booksdf["gender"].value_counts().index.tolist()
count = booksdf['gender'].value_counts()
countList = count.tolist()

# Change F to Female, M to Male in list
for i in range(len(genderList)):
 
    if genderList[i] == 'F':
        genderList[i] = 'Female'
        
    if genderList[i] == 'M':
        genderList[i] = 'Male'
print(genderList)


# Convert country name into iso alpha code 
def findCountry (country_name):
    try:
        return pycountry.countries.get(name=country_name).alpha_3
    except:
        return ("not founded")
booksdf['country'] = booksdf.apply(lambda row: findCountry(row.origin) , axis = 1)

# New df with countries count
originCount = booksdf.groupby(['country']).size()
originCount = originCount.reset_index()
originCount.columns = ["country", "count"]

# Create map 
mapFig = go.Figure(go.Scattergeo())
mapFig = px.scatter_geo(originCount, locations="country", size="count", color_discrete_sequence=['rgb(158,1,66)'])
mapFig.update_geos(projection_type="natural earth")
# mapFig.update_layout(height=400, margin={"r":10,"t":10,"l":10,"b":10})
mapFig.update_layout(title_text="Authors place of birth", font=fontDict, title_x=0.5)
mapFig.update_layout(title_font_color="white")
mapFig.update_layout({
    'plot_bgcolor': '#002b36',
    'paper_bgcolor': '#002b36'
})
mapFig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))

# Greate author gender piechart
#colors = ["#ea5545", "#f46a9b", "#ef9b20", "#edbf33", "#ede15b", "#bdcf32", "#87bc45", "#27aeef", "#b33dc6"]
colors = ['rgb(158,1,66)', 'rgb(213,62,79)', 'rgb(244,109,67)', 'rgb(253,174,97)', 'rgb(254,224,139)', 'rgb(255,255,191)', 'rgb(230,245,152)', 'rgb(171,221,164)', 'rgb(102,194,165)', 'rgb(50,136,189)', 'rgb(94,79,162)']
genPieFig = go.Figure(data=[go.Pie(labels=genderList,
                             values=countList)])
genPieFig.update_traces(hoverinfo='label+percent', textinfo='label', textfont_size=20,
                  marker=dict(colors=colors[2:], line=dict(color='#000000', width=2)))
genPieFig.update_layout(
    title_text="Authors", title_x=0.5)
genPieFig.update(layout_showlegend=False)
genPieFig.update_layout(title_font_color="white",  font=fontDict)
genPieFig.update_layout(title_text="Author")
genPieFig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'
})

# Create genre pie chart
genreCount = booksdf['genre'].value_counts().tolist()
genreList = booksdf["genre"].value_counts().index.tolist()

genrePie = go.Figure(data=[go.Pie(labels=genreList,
                             values=genreCount)])
genrePie.update_traces(hoverinfo='label+percent', textposition='inside', textinfo='label', textfont_size=13,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
genrePie.update_layout(title_text="Genre", title_x=0.5)
genrePie.update(layout_showlegend=False)
genrePie.update_layout(title_font_color="white",  font=fontDict)
genrePie.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'
})

# Create fiction pie chart
fictionCount = booksdf['fiction_nonfiction'].value_counts().tolist()
fictionList = booksdf["fiction_nonfiction"].value_counts().index.tolist()
fictionPie = go.Figure(data=[go.Pie(labels=fictionList,
                             values=fictionCount)])
fictionPie.update_traces(hoverinfo='label+percent', textposition='inside', textinfo='label', textfont_size=13,
                  marker=dict(colors=colors[:2], line=dict(color='#000000', width=2)))
fictionPie.update_layout(
    title_text="Fiction / Non-Fiction", title_x=0.5)
fictionPie.update_layout(title_font_color="white",  font=fontDict)
fictionPie.update(layout_showlegend=False)
fictionPie.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'
})

### Timeline
yearList = booksdf.year.values.tolist()
titleList = booksdf.title.values.tolist()

yearList = pd.to_datetime(pd.Series(yearList), format='%Y')

min_date = date(np.min(yearList).year - 2, np.min(yearList).month, np.min(yearList).day)
max_date = date(np.max(yearList).year + 2, np.max(yearList).month, np.max(yearList).day)

timelineFig, ax = plt.subplots(figsize=(13, 6), constrained_layout=True, facecolor='#002b36')
_ = ax.set_ylim(-1, 1)
_ = ax.set_xlim(min_date, max_date)
_ = ax.axhline(0, xmin=0.05, xmax=0.95, c='#9e0142', zorder=14)
 
_ = ax.scatter(yearList, np.zeros(len(yearList)), s=120, c='#9e0142', zorder=2)
_ = ax.scatter(yearList, np.zeros(len(yearList)), s=30, c='#9e0142', zorder=3)

label_offsets = np.zeros(len(yearList))
label_offsets[::2] = 0.35
label_offsets[1::2] = -0.7
for i, (l, d) in enumerate(zip(titleList, yearList)):
    _ = ax.text(d, label_offsets[i], l, ha='center', rotation = 50, fontfamily='monospace', fontweight='bold', color='white',fontsize=10)

stems = np.zeros(len(yearList))
stems[::2] = 0.3
stems[1::2] = -0.3   
markerline, stemline, baseline = ax.stem(yearList, stems, use_line_collection=True)
_ = plt.setp(markerline, marker=',', color='white')
_ = plt.setp(stemline, color='white')

# hide lines around chart
for spine in ["left", "top", "right", "bottom"]:
    _ = ax.spines[spine].set_visible(False)

# hide tick labels
_ = ax.set_yticks([])

ax.set_facecolor('#002b36')

_ = ax.tick_params(axis='x', color="white", labelcolor="white")

_ = ax.set_title('Original release date', fontweight="bold", fontfamily='monospace', fontsize=16, 
                 color='white')
plt.savefig('timeLine.png')

image_filename = 'timeLine.png' 
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


### Book pages bar chart
groupDf = booksdf.groupby(['title']).mean().reset_index()
count = len(groupDf)

pagesBar = px.bar(booksdf, y='pages', x='title', text_auto='.2s',
            title="Pages per book",
            color_discrete_sequence=colors[:count],
            color="title")
pagesBar.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
pagesBar.update_layout(xaxis={'categoryorder':'total ascending', 'visible':True}, xaxis_title="", yaxis={'visible':False}, title_font_color="white",  font=dict(
        family="monospace",
        size=14,
        color="white"
    ))
pagesBar.update_layout(showlegend=False) 
pagesBar.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'
})

layout = (dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='Map graph',
                figure=mapFig
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='Gender pie chart',
                figure=genPieFig
            )
        ]),
        dbc.Col([
            dcc.Graph(
                id='Genre pie chart',
                figure=genrePie
            )
        ]),
        dbc.Col([
            dcc.Graph(
                id='Fiction pie chart',
                figure= fictionPie
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='pagesBar',
                figure=pagesBar
            )
        ])
        ])
    ])
)
