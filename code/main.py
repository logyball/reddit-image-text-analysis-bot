from os import environ
from time import sleep
import redditBot
import sqlite3

DB_FILE = 'botData.db' # environ['DB_FILE']

def setUpDatabase():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    try:
        cursor.execute("select count(rowid) from processedPosts")
    except sqlite3.OperationalError:
        cursor.execute("create table processedPosts (postName TEXT)")
    try:
        cursor.execute("select count(rowid) from botActions")
    except sqlite3.OperationalError:
        cursor.execute("create table botActions (actionTime INTEGER, action TEXT)")
    cursor.close()

setUpDatabase()
while(1):
    postDict = redditBot.getNewPostInfo()
    #
    #   TODO - some intermediate logic
    #
    if len(postDict) > 0:
        redditBot.makeReply(postDict)
    sleep(60)