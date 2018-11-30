from os import environ
import praw, pprint

SUBR = "cs510bottesting" #environ['SUBREDDIT']
oldPosts = set()    # post IDs that have been addressed already
# DO COMMIT THIS

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
    if (post.post_hint == 'image') or (post.post_hint == 'text'):
        return True
    return False

# returns a list of image posts that haven't been visited yet in 
# the specified subreddit
def getNewImagePosts(red):
    newPosts = []
    subRedInstance = red.subreddit(SUBR)
    for post in subRedInstance.new():
        if (post.name not in oldPosts) and (isImageLink(post)):
            newPosts.append(post)
    return newPosts

# takes the new posts and does some logic with them
def processNewPosts(posts):
    for post in posts:
        postInfo = {}
        postInfo['type'] = post_hint
        url = post.url
        # TODO
        ## 
        # TODO
        print(url)
        oldPosts.add(post.name)

# main logic
#   Called from outside the module, gets an instance of reddit,
#   patrols the subreddit for new posts, then processes them
#   and returns a dict of postID -> {
#                                       'type': 'image' or 'text',
#                                       'url': url,
#                                       'descriptors': [wordList]
#                                   }
#   where wordList is either a list of image descriptors (image post)
#   or a list of words describing the tone of the text (text post)
def getNewPostInfo():
    r = getRedditInstance()
    np = getNewImagePosts(r)
    return processNewPosts(np)