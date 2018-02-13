#
#   This is a bit of code to demonstrate the use of the Search object
#   from the file Search.py
#
# Import some system modues and pieces of the hcde user module.
# The following code depends on these modules.
import sys, json, pickle
from hcde.twitter.Login import Login
from hcde.twitter.Search import Search
from hcde.twitter.auth_settings import *
#
# Creates an authorized login object
app = "HCDE530Test01"
user = "otheralexa"
#
# The next two lines come from auth_settings and help manage keys
app_keys = TWITTER_APP_OAUTH_PAIR(app=app)
app_token_fname = TWITTER_APP_TOKEN_FNAME(app=app)
#
# Creates a login object to authenticate twitter requests
lg = Login(app_name=app, app_user=user, token_fname=app_token_fname)
lg.set_consumer_key(consumer_key=app_keys['consumer_key'])
lg.set_consumer_secret(consumer_secret=app_keys['consumer_secret'])
lg.login()
#
# Create a new search object and set some required
# object values to enable a search
search = Search()
search.set_auth_obj(obj=lg) # Add the authentication object
search.set_user_agent(agent="ie")
search.set_throttling(True) # throttle the requests
search.set_query_result_type(rt="recent")
search.set_page_size(sz=100)
#
# This is the part you expected, we set some search terms, just
# one term in this specific case
terms = "olympics"
search.set_query_terms(terms)
#
# This is really different from the Search.py main() function. In that
# case the code illustrates how to use the Search object with a threaded
# request. In this example below, the code shows how to make a single
# one shot request.
search.make_request()
#
# Once the procedure make_request() returns, there should be some data
# stored in the Search object message queue. We should check the message
# queue to make sure.
print search.messages()
#
# If there are messages then we would want to get one message from
# the queue.
response = search.get_message()
#
# The response is actually a list of dictionary items. While Twitter
# responds with JSON text, the Search object converts each of those
# tweets into an individual Python dictionary. The length of the response
# should be 100, but not always. Twitter does not always give you
# the number of tweets you request. We can see how many we got by
# checking the length of the response.
print len(response)
#
# You could also have a loop that prints each of the tweet dictionary
# items, just so you can see what each tweet dictionary looks like.

# this block of code is pulled from parsing a tweet_text
# we want to use this to parse all the hashtags from the tweets.
def simple_parse_hashtags(tweet=""):
    hash_tags = []
    if tweet:
        token_list = tweet.split()
        for token in token_list:
            if token.startswith('#'):
                hash_tags.append(token)
    return hash_tags

results = []
for tweet in response[:10]:
    # Here, we convert the dictionary back to JSON so that it
    # prints nicely on the screen
	# print json.dumps(tweet,indent=4,sort_keys=True)
	results.append(tweet["text"])
	# Then we dump the data type of the tweet, it should be a dict
	# print type(tweet)
	# print results

for tweet_text in results:
	hashtags = simple_parse_hashtags(tweet_text)
	print "%d %s" %(len(hashtags), tweet_text)

# this will return the same results but in regular expression
# import re
# for tweet_text in results:
# 	hashtags = re.findall(r'(#\S*#|#\S*|\S*#)',tweet_text)
# 	print "%d %s" %(len(hashtags), tweet_text)
#
# Now that we've collected some tweets we need a way to save them.
# One simple way that we saw earlier in class was to use pickle.
# This defines a simple little procedure that opens a file, writes
# the data as a pickle file.
# def pickle_data(fname="",d={}):
#     if( fname ):
#         fout = open(fname, "w")
#         pickle.dump(d,fout)
#         fout.close()
#     else:
#         print "Must supply a file name!"
#     return
# #
# # Using the pickle_data() procedure we can easily save the tweets
# # in the response. Note here that we're saving one whole data structure.
# # The response variable was a Python list that contained up to 100 tweets
# # each of which was a Python dictionary. Pickle is best if you're storing
# # one whole Python data structure, even if that data structure has other
# # data structures within it. Like our response.
# pickle_data("tweets.001.pickle",response)
