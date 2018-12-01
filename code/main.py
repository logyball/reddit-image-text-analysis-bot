from os import environ
import redditBot

postDict = redditBot.getNewPostInfo()
#
#   TODO - some intermediate logic
#
redditBot.makeReply(postDict)