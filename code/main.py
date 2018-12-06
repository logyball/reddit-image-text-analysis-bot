from os import environ
from time import sleep
from model import model
import redditBot
import sqlite3

db = model()
while(1):
    postDict = redditBot.getNewPostInfo()
    #
    #   TODO - some intermediate logic
    #
    if len(postDict) > 0:
        redditBot.makeReply(postDict)
    sleep(60)