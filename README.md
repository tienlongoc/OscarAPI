# OscarAPI Workflow

- Every two hours, query Hacker News API to see if there's any news related to Oscar
- Save Oscar news to database
- At 9am, run query to database to collect the day's Oscar news
- Send newsletter to my email
- Expose flask API to allow getting/updating database information remotely

# Initial context
- Wanted to create some kind of flask API to play with. But needed to find something to populate the relevant database for API to be meaningful. So let's populate it with Oscar news.
