# Script to let us fill our tables with data.

import psycopg
from psycopg.rows import dict_row
from dbinfo import *

def main():
    # Connect to an existing database
    conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=flights user={DBUSER} password={DBPASS}")

    # Open a cursor to perform database operations
    cur = conn.cursor(row_factory=dict_row)

    #cur.execute("DELETE FROM courses")
    #cur.execute("DELETE FROM students")
    #cur.execute("DELETE FROM enroll")


    with open("findGym.csv", 'r') as file:
         with cur.copy(f"COPY indGym FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
            copy.write(file.read())
    conn.commit()
    cur.close()
    conn.close()


main()