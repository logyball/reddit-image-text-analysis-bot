from time import sleep
import redditBot

while(1):
    postDict = redditBot.getNewPostInfo()
    if len(postDict) > 0:
        redditBot.makeReply(postDict)
    sleep(600)
