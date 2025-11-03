# Script to fill tables with data

import psycopg
from psycopg.rows import dict_row
from dbinfo import *

def main():
    conn = psycopg.connect(
        f"host=localhost dbname=gymfinder user={DBUSER} password={DBPASS}"
    )

    cur = conn.cursor(row_factory=dict_row)

    with open("findGym.csv", "r") as file:
        with cur.copy("COPY \"findgym\" FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
            copy.write(file.read())

    conn.commit()
    cur.close()
    conn.close()

    print("Data inserted successfully into FindGym table!")

if __name__ == "__main__":
    main()
