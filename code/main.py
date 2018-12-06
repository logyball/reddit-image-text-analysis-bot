from os import environ
from time import sleep
from model import model
import redditBot
import sqlite3
import pprint

db = model()
while(1):
    postDict = redditBot.getNewPostInfo()
    if len(postDict) > 0:
        pprint.pprint(postDict)
        redditBot.makeReply(postDict)
    sleep(300)