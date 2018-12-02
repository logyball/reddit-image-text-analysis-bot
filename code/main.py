from os import environ
import redditBot
import sqlite3




postDict = redditBot.getNewPostInfo()
#
#   TODO - some intermediate logic
#
redditBot.makeReply(postDict)