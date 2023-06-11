# import pandas as pd
# import numpy as np 

# # Get data from spreadsheet
# sheet_id = "13Jo-MoapyAuYJfCmsrkVeNkdv1NU_fpsIL-bsCYwqZ0"
# sheet_name = "Books"
# bookurl = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
# sheet_name = "Scores"
# scoresurl = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
# booksdf = pd.read_csv(bookurl)
# scoresdf = pd.read_csv(scoresurl) 

# numColumns = ["Readability", "Likability of characters", "Plot", "Made you think", "Writing style", "Overall rating"]

# for column in numColumns:
#     scoresdf[column] = scoresdf[column].astype('string')
#     scoresdf[column] =scoresdf[column].str.replace(',','.')
#     scoresdf[column] = scoresdf[column].astype('float')


# # df = scoresdf.groupby(['Book']).mean().reset_index()

# #newDF = scoresdf.set_index('Member').groupby(level=0).apply(lambda g: np.mean(g.to_numpy()))
# #df = scoresdf.pivot_table(index='Member', aggfunc='mean').mean(axis=1)

# dfOverallScores = scoresdf.pivot_table(index='Member', aggfunc='mean').mean(axis=1)
# dfOverallScores = dfOverallScores.sort_values()

# scoresdfavg = scoresdf.groupby(['Book']).mean().reset_index() 
    


# BestBookdf = scoresdfavg.sort_values(by=['Overall rating'])

# BestBook = BestBookdf.loc[0]
# print(BestBook)

from getData import getData, getOverallAveragesPerBook, getMembers, getBooks


data = getData()

#print(overallAveragePerBook)
booksdf = data["booksdf"]
scoresdf = data["scoresdf"]
list = getMembers(scoresdf)
Booklist = getBooks(booksdf)
overallAveragePerBook = getOverallAveragesPerBook(data["scoresdf"])
import datetime
pagesRead = sum(booksdf['pages']) - booksdf['pages'].iloc[-1]

daysReading = (datetime.datetime.today() - datetime.datetime.strptime("12-03-2022", '%m-%d-%Y')).days
daysReading2 = (booksdf["start_date"].iloc[-1] - booksdf["start_date"].iloc[0]).days

# lastDate = booksdf["Start date"].iloc[-1]
# print(daysReading2)
# pagesRead = sum(booksdf['Pages']) - booksdf['Pages'].iloc[-1]
# daysReading = (booksdf["Start date"].iloc[-1] - booksdf["Start date"].iloc[0]).days
# avgPagesPerDay = pagesRead / daysReading
# print(avgPagesPerDay)
# print(daysReading)
# print(booksdf["Start date"].iloc[-1])

import pandas as pd 
scoresdf = scoresdf.sort_values("book")
# newDf = scoresdf[['member', 'book', 'overall']].copy()
mergedDf = scoresdf.merge(booksdf, left_on=['book'], right_on='title')
mergedDf = mergedDf[['member', 'book', 'overall', 'goodreads_rating']].copy()
mergedDf['diff'] = mergedDf['goodreads_rating'] - mergedDf['overall']
mergedDfGrouped = mergedDf.groupby(['book']).mean().reset_index()
# print(overallAveragePerBook)
# print(scoresdf)



scoresdf['finish'] = scoresdf['finish'].apply(str.upper)
recList = scoresdf["recommend"].value_counts().index.tolist()
recCount = scoresdf['recommend'].value_counts()
recCountList = recCount.tolist()

import plotly.express as px

#readFig = px.bar(scoresdf.groupby(['book']), x='readability', y='book')

# print(scoresdf.groupby(['book']).mean())
print(overallAveragePerBook)