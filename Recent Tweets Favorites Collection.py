from __future__ import print_function

from tweepy import *
from time import sleep
from pandas import DataFrame, read_csv


def load_saved_progress():
    try:
        bad_df = read_csv(bad_filename, usecols=bad_columns)
        start_index = max(bad_df.index) + 1

        try:
            tweet_df = read_csv(tweet_filename, usecols=tweet_columns)
            favorites_df = read_csv(favorites_filename, usecols=favorites_columns)
            user_df = read_csv(user_filename, usecols=user_columns)

        except IOError:
            tweet_df = None
            favorites_df = None
            user_df = None

    except IOError:
        tweet_df = None
        favorites_df = None
        user_df = None
        bad_df = None
        start_index = 0

    return start_index, tweet_df, favorites_df, user_df, bad_df

def save_progress():
    for df_data, df_cols, filename in (
        (tweet_tuples, tweet_columns, tweet_filename),
        (favorites_tuples, favorites_columns, favorites_filename),
        (user_tuples, user_columns, user_filename),
        (bad_accounts, bad_columns, bad_filename)):
        data_df = DataFrame(df_data, columns=df_cols)
        data_df.to_csv(filename, encoding='utf-8', index=False)

tweet_filename = ""
favorites_filename = ""
user_filename = ""
bad_filename = ""

tweet_columns = ['Creation Date', 'Author', 'Text',
                 'Favorite Count', 'Retweet Count']
favorites_columns = ['Favoriter Username', 'Creation Date', 'Author',
                     'Text', 'Favorite Count', 'Retweet Count']
user_columns = ['Username', 'User ID', 'Account Creation Date',
                'Friend Count', 'Follower Count', 'Organizations']
bad_columns = ['Username', 'User ID', 'Error Message']

print("Establishing API Access...")

consumer_key = ""
consumer_secret = ""
access_token = ""
access_secret = ""

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = API(auth)

print("API Access Successfully Established!\n")
print("Setting Up Appropriate Variables...")

accounts_filename = ""
accounts_df = read_csv(accounts_filename)

start_index, tweet_df, favorites_df, user_df, bad_df = load_saved_progress()

bad_accounts = []

TIMEOUT = 15
CUTOFF = 3

tweet_tuples = []
favorites_tuples = []
user_tuples = []

print("Variables Successfully Set Up!\n")
print("Processsing User Data...")

for user_index in accounts_df.index:
    print("   Processing User Index {index}...".format(index=user_index))

    username = accounts_df['Username'][user_index]

    RTS = api.rate_limit_status()

    if RTS['resources']['application']['/application/rate_limit_status']['remaining'] < CUTOFF or \
       RTS['resources']['users']['/users/show/:id']['remaining'] < CUTOFF or \
       RTS['resources']['statuses']['/statuses/user_timeline']['remaining'] < CUTOFF or \
       RTS['resources']['favorites']['/favorites/list']['remaining'] < CUTOFF or \
       RTS['resources']['friends']['/friends/list']['remaining'] < CUTOFF or \
       RTS['resources']['followers']['/followers/list']['remaining'] < CUTOFF or \
       RTS['resources']['lists']['/lists/memberships']['remaining'] < CUTOFF:

        print("\n   WARNING: Close to a Resource Limit --> "
              "Sleeping for {amount} Minutes...\n".format(amount=TIMEOUT))

        sleep(TIMEOUT * 60)

    try:
        # check: does the user still exist?
        # if so, retrieve the remaining information
        user = api.get_user(screen_name=username)

        user_id = user.id_str
        creation_date = user.created_at
        friend_count = user.friends_count
        follower_count = user.followers_count

        orgs = [org.name for org in api.lists_memberships(screen_name=username)]

        recent_tweets = api.user_timeline(screen_name=username, count=200)
        recent_favorites = api.favorites(id=username, page=1)

# Possible Reasons for Failure (i.e. TweepError is Thrown)
# --------------------------------------------------------
#
# 1) User does not exist or has been suspended
# 2) User is protected --> cannot access (i.e. not authorized) to access data
# 3) Personal authentication has expired, in particular access tokens

    except TweepError, TweepErrorMessage:
        user_id = accounts_df['Twitter ID'][user_index]

        # for nicer formatting of the TweepErrorMessage
        try:
            message = TweepErrorMessage.message[0]['message']

        except:
            message = str(TweepErrorMessage)

        bad_accounts.append((username, user_id, message))

        print("   User Index {index} Processing FAILED: {message}\n".format(
            index=user_index, message=message))

        continue

    bad_accounts.append((username, user_id, "SUCCESSFUL PROCESSING"))
    user_tuples.append((username, user_id, creation_date,
                        friend_count, follower_count, orgs))

    for index in range(len(recent_tweets)):
        tweet = recent_tweets[index]

        date = tweet.created_at
        author = tweet.author.screen_name
        text = tweet.text
        favorite_count = tweet.favorite_count
        retweet_count = tweet.retweet_count

        tweet_tuples.append((date, author, text,
                             favorite_count, retweet_count))

    for index in range(len(recent_favorites)):
        favorite = recent_favorites[index]

        date = favorite.created_at
        author = favorite.author.screen_name
        text = favorite.text
        favorite_count = favorite.favorite_count
        retweet_count = favorite.favorite_count

        favorites_tuples.append((username, date, author, text,
                                 favorite_count, retweet_count))

    save_progress()

    print("   User Index {index} "
          "Processing Complete!\n"
          .format(index=user_index))

print("User Data Processing Complete!\n")
print("Processing and Saving Data...")

save_progress()

print("Data Processing and Saving Complete!")
