from dotenv import load_dotenv
load_dotenv()

import pandas as pd 
import pandas as pd
import mysql.connector
import os

dbHost     = os.environ.get("DATABASE_HOST")
dbUser     = os.environ.get("DATABASE_USER")
dbPassword = os.environ.get("DATABASE_PASSWORD")
dbName     = os.environ.get("DATABASE_NAME")

# pull data from db, put in df 
mydb = mysql.connector.connect(
  host=dbHost,
  user=dbUser,
  password=dbPassword,
  database=dbName
)

mycursor = mydb.cursor()

def getData():

    sql = "SELECT * FROM books ORDER BY start_date;"
    booksdf = pd.read_sql(sql, mydb)

    sql = "SELECT * FROM scores"
    scoresdf = pd.read_sql(sql, mydb)
    
    sql = "SELECT * FROM summaries"
    sumdf = pd.read_sql(sql, mydb)
       
    # #Adjust datatypes etc. 
    convert_dict = {
        'isbn': str,
        'title': str,
        'author': str,
        'gender': str,
        'origin': str,
        'pages': int,
        'year': int,
        'genre': str,
        'fiction_nonfiction': str,
        'goodreads_rating': float,
        'images': str,
        'goodreads_code': str,
        'googleCat': str,
        'textSnippet': str
    } 
    booksdf = booksdf.astype(convert_dict)
    
    booksdf['start_date'] = pd.to_datetime(booksdf['start_date'], dayfirst=True)
    booksdf['end_date'] = pd.to_datetime(booksdf['end_date'], dayfirst=True)
 
    convert_dict = {
        'member': str,
        'book': str,
        'readability': float,
        'likability': float,
        'plot': float,
        'madeyouthink': float,
        'writingstyle': float,
        'overall': float,
        'recommend': str,
        "finish": str} 
    
    scoresdf = scoresdf.astype(convert_dict)
    
    convert_dict = {
        'isbn': str,
        'grCode': str,
        'title': str,
        'summary': str
    }
    
    sumdf = sumdf.astype(convert_dict)
              
    return {
        "booksdf": booksdf,
        "scoresdf": scoresdf,
        "sumdf": sumdf
    }



def getMembers(scoresdf):
    return scoresdf.member.unique().tolist()

def getBooks(booksdf):
    return booksdf.title.unique().tolist()

# Average scores for each book for each categorie
# Returns df with one score per book per categorie
def getOverallAveragesPerBook(scoresdf):
    overallAveragesPerBook = scoresdf.groupby(['book']).mean().reset_index() 
    return overallAveragesPerBook.sort_values(by=['overall'], ignore_index = True)

# Calculate average score given on all categories on every book per member
# Returns one score per member
def getOverallAveragePerMember(scoresdf):
    dfOverallScores = scoresdf.pivot_table(index='member', aggfunc='mean').mean(axis=1)
    return dfOverallScores.sort_values()
