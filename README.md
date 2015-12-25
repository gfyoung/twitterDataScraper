# twitterDataScraper
Python Twitter API Data Scraper

## How it works
- Takes in a provided CSV file (```accounts_filename```) of usernames and Twitter IDs
- For each username and Twitter ID, the scraper obtains the following information:
  - User Information
    - ```Username```: User's username
    - ```User ID```: Users's user ID
    - ```Account Creation Date```: When the account was created
    - ```Friend Count```: How many friend the user has
    - ```Follower Count```: How many followers the user has
    - ```Organizations```: How many organizations the user is a part of

  - User Tweet Information
    - ```Creation Date```: When the tweet was created
    - ```Author```: The author of the tweet (i.e. the user)
    - ```Text```: The text of the tweet
    - ```Favorite Count```: How many times the tweet was favorited
    - ```Retweet Count```: How many times the tweet was retweeted
  
  - User Favorited Information
    - ```Favoriter Username```: The username of the user who favorited the tweet (i.e. the user)
    - ```Creation date```: When the tweet was created
    - ```Author```: The author of the tweet
    - ```Text```: The text of the tweet
    - ```Favorite Count```: How many times the tweet was favorited
    - ```Retweet Count```: How many times the tweet was retweeted

- However, perhaps due to API issues or changes in user status, certain users may not have this information, or they may
  no longer exist at all! Thus, the code also provides a log of the scraper's success in querying a particular user. The columns are:
  - ```Username```: The username of the user
  - ```User ID```: The Twitter ID of the user
  - ```Error message```: A status message indicating the success of the scraper in obtaining information about the user

- If there are a large number of usernames to query, most likely you will encounter a timeout with Twitter's API, as it
  imposes limits on how often you can query certain information. Before querying the next user, the code checks whether or
  not it is getting close to overstepping one of those limits. If so, the code will pause for an appropriate period of time
  before querying once more.

- To protect against unexpected events, such as computer/machine shutdown or other unaccounted for exceptions/error while the
  code is running, the progress of the scraping is saved after every user. Thus, if the code has to be rerun again, the code will
  just resume from the last user it queried.

- <b>NOTE</b>: In order for this code to run successfully, it required authentication with the Twitter API as well as a data file
  of usernames and Twitter IDs. If any of this information is omitted or incorrectly provided, the script will not work!
  
