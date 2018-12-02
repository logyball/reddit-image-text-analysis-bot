from os import environ
from googleMl import googleTextAnalysis, googleImageAnalysis
import praw, pprint

SUBR = "cs510bottesting" #environ['SUBREDDIT']
oldPosts = set()    # post IDs that have been addressed already

USERNAME = environ['BOT_USERNAME']
PASSWORD = environ['BOT_PASSWORD']
CLIENT_ID = environ['BOT_CLIENT_ID']
CLIENT_SECRET = environ['BOT_CLIENT_SECRET']

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

# returns a list of image posts that haven't been visited yet in 
# the specified subreddit
def getNewTextOrImagePosts(red):
    newPosts = []
    subRedInstance = red.subreddit(SUBR)
    for post in subRedInstance.new():
        #pprint.pprint(vars(post))
        if (post.name not in oldPosts):
            postType = isImageOrText(post)
            if postType is not None:
                newPosts.append((post, postType))
    return newPosts

# returns list of strings, best guess info based on the 
# google ML APIs.  Image gets descriptors, text gets tone
def googleMlWrapper(postData):
    if postData[1] == "txt":
        return googleTextAnalysis(postData[0].selftext)
    return googleImageAnalysis(postData[0].url)

# takes the new posts and does some logic with them
# newPosts is a list of posts, posts is a tuple
# (post Object, postType String)
def processNewPosts(posts):
    postsToSend = {}
    for post in posts:
        postInfo = {}
        postInfo['type'] = post[1]
        postInfo['title'] = post[0].title
        postInfo['id'] = post[0].id
        postInfo['url'] = post[0].url
        postInfo['wordList'] = googleMlWrapper(post)
        postsToSend[post[0].name] = postInfo
        oldPosts.add(post[0].name)
    return postsToSend

# TODO - implement a reply based on the info we have post-processing
def buildReply(postInfo):
    reply = "these are some interesting words:"
    for w in postInfo['wordList']:
        reply = reply + " " + w
    return reply
    # TODO - incoporate additional logic

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
    for post in postsToReplyTo:
        text = buildReply(postsToReplyTo[post])
        sub = r.submission(id=postsToReplyTo[post]['id'])
        sub.reply(text)