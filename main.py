from os import environ
import praw, pprint

USERNAME = environ['BOT_USERNAME']
PASSWORD = environ['BOT_PASSWORD']
CLIENT_ID = environ['BOT_CLIENT_ID']
CLIENT_SECRET = environ['BOT_CLIENT_SECRET']
oldPosts = set()    # posts that have been addressed already
SUBR = "cs510bottesting" #environ['SUBREDDIT']

# reddit API
def getRedditInstance():
    return praw.Reddit(client_id=CLIENT_ID,
                       client_secret=CLIENT_SECRET,
                       username=USERNAME,
                       password=PASSWORD,
                       user_agent='testscript, contact loganballard@gmail.com')

# returns whether or not the posted url is a image
def isImageLink(post):
    if post.post_hint == 'image':
        return True
    return False

# returns a list of image posts that haven't been visited yet in 
# the specified subreddit
def getNewImagePosts(red):
    newPosts = []
    subRedInstance = red.subreddit(SUBR)
    for post in subRedInstance.new():
        if (post not in oldPosts) and (isImageLink(post)):
            newPosts.append(post)
    return newPosts

r = getRedditInstance()
print(getNewImagePosts(r))
print(oldPosts)