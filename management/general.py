import sqlite3
import random
from config import general_database
from management.position import positionof
from management.db import db_set

conn = sqlite3.connect(general_database)
c = conn.cursor()

def add_activity(user_id,user_name):
    """Increase the activity score of a player."""
    c.execute("SELECT * FROM 'activity' WHERE id =?",(user_id,))
    if c.fetchone() == None:
        c.execute("INSERT INTO 'inventory'('id','name') VALUES (?,'?');",(user_id,user_name))
        c.execute("INSERT INTO 'activity'('id','name') VALUES (?,'?');",(user_id,user_name))
        c.execute("INSERT INTO 'users'('id','name') VALUES (?,'?');",(user_id,user_name))
    c.execute("UPDATE 'activity' SET spam_activity = spam_activity + 1 WHERE id =?",(user_id,))
    conn.commit()
    db_set(user_id,'name',user_name)

def purge_activity():
    """Purge the activity score of all players."""
    c.execute("UPDATE activity SET spam_activity = 0 WHERE spam_activity > 2*spam_filter;")
    c.execute("UPDATE activity SET activity = activity + spam_activity*spam_activity/-spam_filter + 2*spam_activity;")
    c.execute("UPDATE activity SET activity = activity*0.9958826236;")
    c.execute("UPDATE activity SET spam_activity=0")
    c.execute("UPDATE activity SET record_activity = activity WHERE record_activity < activity;")

    c.execute("UPDATE users SET activity = (SELECT activity.activity FROM activity WHERE activity.id = users.id);")
    conn.commit()

def deal_credits():
    """Give all players a small portion of credits based on their activity."""
    c.execute("UPDATE users SET credits = credits + CAST( activity/500 AS INTEGER);")
    conn.commit()