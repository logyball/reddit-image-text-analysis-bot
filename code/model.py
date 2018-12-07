"""
Simple DB model
"""

import sqlite3
from time import time
DB_FILE = 'DB.db' # environ['DB_FILE']

class model():
    def __init__(self):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        try: 
            cur.execute("select count(rowid) from botActions")
            cur.execute("select count(rowid) from processedPosts")
        except sqlite3.OperationalError:
            cur.execute("create table botActions(postId text, action text, time int)")
            cur.execute("create table processedPosts(postId text, link text)")
        cur.close()
    
    def addBotAction(self, action, postId=None):
        """
        Add record of a bot action to the DB
        """
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        intTime = int(time())
        cur.execute("insert into botActions(postId, action, time) VALUES (?,?,?)", (postId, action, intTime))
        conn.commit()
        cur.close()

    def addToOldPost(self, postId, link):
        """
        Add an entry in DB to keep track of already processed posts
        """
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("insert into processedPosts(postID, link) VALUES (?,?)", (postId, link))
        conn.commit()
        cur.close()


    def isOldPost(self, postId):
        """
        Check if a post has already been processed
        """
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM processedPosts WHERE postId = '%s'" % postId)
        row = cur.fetchone()
        if row is not None:
            cur.close()
            return True
        else:
            cur.close()
            return False

    def select(self):
        """
        Query the DB for a list of actions to print to the Front-End website
        """
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM botActions LEFT JOIN processedPosts on botActions.postID = processedPosts.postID")
        return cur.fetchall()

