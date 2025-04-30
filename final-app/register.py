# Script to let us register students.

import psycopg
from psycopg.rows import dict_row
from dbinfo import *
from nicegui import ui, app

#from page_protected import protected
#from page_dashboard import dashboard

# Connect to an existing database
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=flights user={DBUSER} password={DBPASS}")

# Open a cursor to perform database operations
cur = conn.cursor(row_factory=dict_row)

def get_user():
    cur.execute("SELECT user_id, name, age, weight, goal, allergy, streak, playlist FROM USERS")
    rows = cur.fetchall()
    return rows


ui.run(reload=False, storage_secret='THIS_NEEDS_TO_BE_CHANGED')
