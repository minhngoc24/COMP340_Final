# Script to let us fill our tables with data.

import psycopg
from psycopg.rows import dict_row
from dbinfo import *

def main():
    # Connect to an existing database
    conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")

    # Open a cursor to perform database operations
    cur = conn.cursor(row_factory=dict_row)

    #cur.execute("DELETE FROM courses")
    #cur.execute("DELETE FROM students")
    #cur.execute("DELETE FROM enroll")

    with open("findGym.csv.csv", 'r') as file:
         with cur.copy(f"COPY findGym FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
            copy.write(file.read())
    conn.commit()

    with open("gyms.csv.csv", 'r') as file:
        with cur.copy(f"COPY gyms FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
            copy.write(file.read())
    conn.commit()

    with open("hasIngredients.csv", 'r') as file:
        with cur.copy(f"COPY hasIngredients FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
            copy.write(file.read())
    conn.commit()

    with open("Ingredients.csv.csv", 'r') as file:
        with cur.copy(f"COPY Ingredients FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
            copy.write(file.read())
    conn.commit()

    with open("makeRecipe.csv.csv", 'r') as file:
        with cur.copy(f"COPY makeRecipe FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
            copy.write(file.read())
    conn.commit()

    with open("Match.csv", 'r') as file:
        with cur.copy(f"COPY Match FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
            copy.write(file.read())
    conn.commit()

    with open("pt.csv.csv", 'r') as file:
        with cur.copy(f"COPY pt FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
            copy.write(file.read())
    conn.commit()

    with open("recipes.csv.csv", 'r') as file:
        with cur.copy(f"COPY recipes FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
            copy.write(file.read())
    conn.commit()

    with open("ReviewGym.csv", 'r') as file:
        with cur.copy(f"COPY ReviewGym FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
            copy.write(file.read())
    conn.commit()

    with open("ReviewPT.csv.csv", 'r') as file:
        with cur.copy(f"COPY ReviewPT FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
            copy.write(file.read())
    conn.commit()

    with open("reviewRecipes.csv.csv", 'r') as file:
        with cur.copy(f"COPY reviewRecipes FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
            copy.write(file.read())
    conn.commit()

    with open("users.csv", 'r') as file:
        with cur.copy(f"COPY users FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
            copy.write(file.read())
    conn.commit()

    with open("WorkInGym", 'r') as file:
        with cur.copy(f"COPY WorkInGym FROM STDIN WITH (FORMAT CSV, HEADER true)") as copy:
            copy.write(file.read())
    conn.commit()

main()