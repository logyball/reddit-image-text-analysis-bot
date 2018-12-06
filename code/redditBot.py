from os import environ
from googleMl import googleTextAnalysis, googleImageAnalysis
from time import time
from model import model
from gify_query import query_giphy
from query_spotify import get_a_playlist
import praw, pprint, sqlite3

SUBR = environ['SUBREDDIT']
USERNAME = environ['BOT_USERNAME']
PASSWORD = environ['BOT_PASSWORD']
CLIENT_ID = environ['BOT_CLIENT_ID']
CLIENT_SECRET = environ['BOT_CLIENT_SECRET']

DB = model()

# reddit API
def getRedditInstance():
    return praw.Reddit(client_id=CLIENT_ID,
                       client_secret=CLIENT_SECRET,
                       username=USERNAME,
                       password=PASSWORD,
                       user_agent='testscript, contact loganballard@gmail.com')

# returns whether or not the posted url is a image
def isImageOrText(post):
    if post.is_self:
        return "txt"
    elif (post.post_hint is not None) and (post.post_hint == 'image'):
        return "img"
    return None

def makeLinkToPost(permalink):
    link = "www.reddit.com" + permalink
    return link

# returns a list of image posts that haven't been visited yet in 
# the specified subreddit
def getNewTextOrImagePosts(red):
    DB.addBotAction("scanning for new posts...")
    newPosts = []
    subRedInstance = red.subreddit(SUBR)
    for post in subRedInstance.new():
        if not DB.isOldPost(post.name):
            postType = isImageOrText(post)
            if postType is not None:
                newPosts.append((post, postType))
    return newPosts

# returns list of strings, best guess info based on the 
# google ML APIs.  Image gets descriptors, text gets tone
def googleMlWrapper(postData):
    if postData[1] == "txt": 
        DB.addBotAction("Sending new text post to google NLP ML API...", postId=postData[0].name)
        return googleTextAnalysis(postData[0].selftext)
    DB.addBotAction("Sending new image post to google vision ML API...", postId=postData[0].name)
    return googleImageAnalysis(postData[0].url)

# takes the new posts and does some logic with them
# newPosts is a list of posts, posts is a tuple
# (post Object, postType String)
def processNewPosts(posts):
    if len(posts) > 0:
        DB.addBotAction("New posts found! Processing...")
    else:
        return {}
    postsToSend = {}
    for post in posts:
        vars(post[0]) # make reddit api return all vars
        postInfo = {}
        postInfo['permalink'] = post[0].permalink
        postInfo['type'] = post[1]
        postInfo['title'] = post[0].title
        postInfo['id'] = post[0].id
        postInfo['url'] = post[0].url
        postInfo['wordList'] = googleMlWrapper(post)
        postsToSend[post[0].name] = postInfo
    return postsToSend

# implement a reply based on the info we have post-processing
def buildReply(postInfo):
    reply = "I've analyzed your post and come up with some interesting words "
    reply = reply + "based on google's ML APIs.  These words that are relevant are: "
    for word in postInfo['wordList']:
        reply = reply + word + " "
    reply = reply + ". "
    if postInfo['playlist'] is not None:
        reply = reply + "Here's a spotify playlist I found based on the query " + postInfo['query'] +": "
        reply = reply + postInfo['playlist']
        reply = reply + " . "
    if postInfo['gif'] is not None:
        reply = reply + "Here's a gif from Giphy based on the query "+ postInfo['query'] +": "
        reply = reply + postInfo['gif'] + " ."
    return reply

# initial logic
#   Called from outside the module, gets an instance of reddit,
#   patrols the subreddit for new posts, then processes them
#   and returns a dict of postID -> {
#                                       'type': 'img' or 'txt',
#                                       'title: post title
#                                       'url': url,
#                                       'wordList': [list of descriptors]
#                                   }
#   where wordList is either a list of image descriptors (image post)
#   or a list of words describing the tone of the text (text post)
def getNewPostInfo():
    r = getRedditInstance()
    np = getNewTextOrImagePosts(r)
    return processNewPosts(np)

# followUp logic
#   After all the proocessing of each post, post a reply to each 
#   thread based on the post-processed info
def makeReply(postsToReplyTo):
    r = getRedditInstance() # in case we forgot
    DB.addBotAction("Replying to new posts...")
    for post in postsToReplyTo:
        Query = postsToReplyTo[post]['wordList'][1]
        postsToReplyTo[post]['query'] = Query
        postsToReplyTo[post]['playlist'] = get_a_playlist(Query)
        postsToReplyTo[post]['gif'] = query_giphy(Query)
        text = buildReply(postsToReplyTo[post])
        sub = r.submission(id=postsToReplyTo[post]['id'])
        comment = sub.reply(text)
        DB.addToOldPost(post, makeLinkToPost(postsToReplyTo[post]['permalink']))
    DB.addBotAction("Done Replying! Going back to sleep...")
