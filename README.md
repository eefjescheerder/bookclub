# bookclub

## Where the data in this project is coming from

Information about the books and the scores given to every book are stored in a Google Sheet.
[image]
[image]


The image and text snippet are being collected through the Google Book API, using the ISBN. 

The reviews that are being used for the wordcloud and average summary on the book details pages are scraped from [GoodReads.com](http://GoodReads.com) using the Goodreads identifyer. 

Challenges with this project: 

The Google book API doesn’t always deliver flawless information. Pages and Original release date aren’t always accurate. Therefore these details need to be filled in manually in the Google sheet. 

Dash does not offer a way to create a timeline in such a way that is useful for this particular project. Therefore I had to use Matplotlib, which has its implications when using it in an interactive dashboard. 

Room for improvement:

Alle reviews in database stored before cleaning the text

- Writing a script that automatically scrapes the Goodreads identifier, based on the ISBN.
- Using Lambda, writing a function that gets triggered every time a new book, or new scores have been added to the Google Sheet.
- More meaningful information in the tooltips

Future development ideas:

Feed all reviews to openai to generate the average summary for each book. 

Making the matplotlib timelime on the “Books” page interactive so that you can easily zoom in on a particular time frame. 
Write script that uses the thumbnail to Google image search a book cover image in higher resolution. 

When the list with books gets longer, I will not be able to show all of the books in the bar charts. Therefore, there should be another dropdown on the ‘Scores’ pages with the options ‘Top 10’ and ‘Bottom 10’.
