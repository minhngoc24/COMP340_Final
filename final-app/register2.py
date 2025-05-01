# Script to let us register students.

import psycopg
#from aext_shared import user_id
from psycopg.rows import dict_row
#from xarray.core.weighted import Weighted

from dbinfo import *
from nicegui import ui, app
#from page_protected import protected
#from page_dashboard import dashboard #


# Connect to an existing database
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=flights user={DBUSER} password={DBPASS}")


# Open a cursor to perform database operations
cur = conn.cursor(row_factory=dict_row)


def get_user():
   cur.execute("SELECT user_id, name, age, weight, goal, allergy, streak, playlist FROM USERS")
   rows = cur.fetchall()
   return rows


@ui.page('/')
def homepage():
   ui.label("Welcome to the homepage!")
   ui.link("Login", '/login')


   username = app.storage.user.get('username', None)  # default if not logged in is None
   if username is not None:
       ui.label("You are logged in as user: " + username)


       cur.execute('SELECT weight, playlist_genre, fitness_goal FROM USERS WHERE user_id = %s', (username,))
       row = cur.fetchone()
       weight = row['weight']
       playlist_genre = row['playlist_genre']
       fitness_goal = row['fitness_goal']




       playlist_result = ui.label('')
       result = ui.label('')
       goal_result = ui.label('')

       def get_recipes():
           def hide_table():
               recipe_card.set_visibility(False)


           cur.execute("SELECT * FROM Recipes")
           rows = cur.fetchall()
           with ui.card() as recipe_card:
               ui.label("Recipes")
               cols = [{'name': 'rid', 'field': 'rid', 'label': "Recipe ID"},
                       {'name': 'description', 'field': 'description', 'label': "Desc"},
                       {'name': 'meal_name', 'field': 'meal_name', 'label': "Meal Name"},
                       {'name': 'calories', 'field': 'calories', 'label': "Calories"},
                       {'name': 'prep_time', 'field': 'prep_time', 'label': "Time"}]
               recipe_table = ui.table(columns=cols, rows=[])
               ui.button('Hide Table', on_click=hide_table)


           recipe_table.add_rows(rows)
           recipe_table.update()
           recipe_card.set_visibility(True)




       def visible_change_weight():
           weight_card.set_visibility(True)


       def visible_change_playlist():
           playlist_card.set_visibility(True)




       def visible_change_goal():
           goal_card.set_visibility(True)


       def visible_find_gym():
           findgym_card.set_visibility(True)

       def visible_find_pt():
           findpt_card.set_visibility(True)

       def get_my_recipes():
           def hide_my_table():
               recipe_card.set_visibility(False)

           cur.execute(
               "SELECT * FROM MakeRecipes natural join USERS natural join Recipes where MakeRecipes.user_id = %s", [username])
           rows = cur.fetchall()
           with ui.card() as recipe_card:
               ui.label("My Recipes")
               cols = [{'name': 'rid', 'field': 'rid', 'label': "Recipe ID"},
                       {'name': 'description', 'field': 'description', 'label': "Desc"},
                       {'name': 'meal_name', 'field': 'meal_name', 'label': "Meal Name"},
                       {'name': 'calories', 'field': 'calories', 'label': "Calories"},
                       {'name': 'prep_time', 'field': 'prep_time', 'label': "Time"}]
               recipe_table = ui.table(columns=cols, rows=[])
               ui.button('Hide Table', on_click=hide_my_table)
               recipe_table.add_rows(rows)
               recipe_table.update()
               recipe_card.set_visibility(True)


       ui.button('Change Weight', on_click= visible_change_weight)
       ui.button('Change Playlist', on_click=visible_change_playlist)
       ui.button('Change Goal', on_click=visible_change_goal)
       ui.button('Search Recipes', on_click=get_recipes)
       ui.button('Get my recipes', on_click=get_my_recipes)
       ui.button('Find gyms within a radius', on_click=visible_find_gym)
       ui.button('Find your Personal Trainer', on_click=visible_find_pt)

       def update_weight():
           if user_box_weight.value == username and newweight_box.value:
               cur.execute('UPDATE USERS SET weight = %s WHERE user_id = %s',
                           (newweight_box.value, user_box_weight.value))
               conn.commit()
               print(f"Current weight is: {newweight_box.value}")
               result.text = f"New weight is: {newweight_box.value}"
               weight_card.set_visibility(False)
           else:
               result.text = 'Please enter a valid user ID and weight.'


       with ui.card() as weight_card:
           user_box_weight = ui.input('User ID:')
           newweight_box = ui.input('New Weight:')
           ui.button('Confirm weight', on_click=update_weight)
       weight_card.set_visibility(False)


       def update_playlist():
           if user_box_playlist.value == username and newPlaylist_box.value:
               cur.execute('UPDATE USERS SET playlist_genre = %s WHERE user_id = %s',
                           (newPlaylist_box.value, user_box_playlist.value))
               conn.commit()
               print(f"Current playlist is: {newPlaylist_box.value}")
               playlist_result.text = f"New playlist is: {newPlaylist_box.value}"
               playlist_card.set_visibility(False)


           else:
               playlist_result.text = 'Please enter a valid playlist'




       with ui.card() as playlist_card:
           user_box_playlist = ui.input('User ID:')
           newPlaylist_box = ui.input('New Playlist:')
           ui.button('Confirm playlist', on_click=update_playlist)
       playlist_card.set_visibility(False)


       def update_goal():
           if user_box_goal.value == username and newGoal_box.value:
               cur.execute('UPDATE USERS SET fitness_goal = %s WHERE user_id = %s',
                           (newGoal_box.value, user_box_goal.value))
               conn.commit()
               print(f"Current goal is: {newGoal_box.value}")
               goal_result.text = f"New goal is: {newGoal_box.value}"
               goal_card.set_visibility(False)


           else:
               goal_result.text = 'Please enter a valid playlist'


       with ui.card() as goal_card:
           user_box_goal = ui.input('User ID:')
           newGoal_box = ui.input('New Goal:')
           ui.button('Confirm goal', on_click=update_goal)
       goal_card.set_visibility(False)


       add_recipe_result = ui.label('')


       def visible_add_recipe():
           add_recipe_card.set_visibility(True)


       ui.button('Add a New Recipe', on_click=visible_add_recipe)


       def confirm_add_recipe():
           try:
               rid = int(rid_input.value)
               description = description_input.value
               meal_name = meal_name_input.value
               calories = int(calories_input.value)
               prep_time = int(prep_time_input.value)


               # Insert into recipes
               cur.execute(
                   "INSERT INTO recipes (rid, description, meal_name, calories, prep_time) VALUES (%s, %s, %s, %s, %s)",
                   (rid, description, meal_name, calories, prep_time))
               cur.execute("INSERT INTO makerecipes(user_id, rid) VALUES (%s, %s)", (username, rid))
               conn.commit()


               conn.commit()


               add_recipe_result.text = f"Recipe '{meal_name}' added and marked as made!"
               add_recipe_card.set_visibility(False)


           except Exception as e:
               conn.rollback()
               add_recipe_result.text = f" Error: {str(e)}"


       with ui.card() as add_recipe_card:
           rid_input = ui.input('Recipe ID (Rid)')
           description_input = ui.input('Description')
           meal_name_input = ui.input('Meal Name')
           calories_input = ui.input('Calories')
           prep_time_input = ui.input('Prep Time (minutes)')
           ui.button('Add Recipe', on_click=confirm_add_recipe)


       add_recipe_card.set_visibility(False)

       with ui.card() as findpt_card:
           get_user = ui.input('Enter user ID to look up PT:')
           pt_results = ui.column()

           def find_pts():
               if get_user.value.isdigit():
                   # Step 1: Get PT info
                   cur.execute('''
                      SELECT p.name, p.experience, p.phone
                      FROM match m
                      JOIN pt p ON m.pt_id = p.pt_id
                      WHERE m.user_id = %s
                  ''', (get_user.value,))
                   pt_row = cur.fetchone()

                   cur.execute('SELECT fitness_goal FROM users WHERE user_id = %s', (get_user.value,))
                   user_row = cur.fetchone()

                   pt_results.clear()
                   with pt_results:
                       if pt_row and user_row:
                           ui.label(f" {pt_row['name']} — {pt_row['experience']} yrs experience,  {pt_row['phone']}")
                           ui.label(f" Helping you achieve your goal: {user_row['fitness_goal']}")
                       else:
                           ui.label("PT or goal not found for that user.")
               else:
                   pt_results.clear()
                   with pt_results:
                       ui.label("Please enter a valid user ID.")

           ui.button('Show PT', on_click=find_pts)

       findpt_card.set_visibility(False)

       with ui.card() as findgym_card:
           radius_input = ui.input('Enter radius:')
           gym_results = ui.column()


           def find_gym():
               if radius_input.value.isdigit():
                   radius = int(radius_input.value)
                   cur.execute('SELECT gym_address, radius FROM findgym WHERE radius <= %s', (radius,))
                   rows = cur.fetchall()
                   gym_results.clear()
                   with gym_results:
                       if rows:
                           for row in rows:
                               ui.label(f"{row['gym_address']} (Radius: {row['radius']})")
                       else:
                           ui.label("No gyms found within that radius.")
               else:
                   gym_results.clear()
                   with gym_results:
                       ui.label("Please enter a valid user ID and radius.")


           ui.button('Confirm Radius', on_click=find_gym)


       findgym_card.set_visibility(False)





   else:
       ui.label("You are not logged in.")




   ui.link("Login", '/login')
   ui.link("Logout", '/logout')
   #ui.link("Password-protected test page", '/protected')
   #ui.link("Dashboard", '/dashboard')

@ui.page('/login')
def login(redirect_url = '/'):

   def try_login():
       password = get_password_for_user(username_box.value)
       if password == password_box.value:
           app.storage.user['username'] = username_box.value
           ui.navigate.to(redirect_url)  # go to where the user wanted to go
       else:
           ui.notify('Wrong username or password', color='negative')


   #if app.storage.user.get('authenticated', False):
   #        return RedirectResponse('/')
   ui.label("Use a user_id number for username and the grad year for password.")
   with ui.row().classes('items-center'):
       username_box = ui.input('Username:')
       password_box = ui.input('Password', password=True, password_toggle_button=True)
       ui.button('Log in', on_click=try_login)




def get_password_for_user(user_id):
   cur.execute("SELECT age from USERS where user_id=%s", [user_id])
   row = cur.fetchone()
   return str(row['age'])  # return as a string to simulate a password


def get_weight_for_user(user_id):
   cur.execute("SELECT weight from USERS where user_id=%s", [user_id])
   row = cur.fetchone()
   return str(row['weight'])  # return as a string to simulate a password


@ui.page('/logout')
def logout():
   app.storage.user.pop('username')
   ui.label("You are now logged out.")
   ui.link("Back to homepage", '/')
   #ui.button('Register!', on_click=lambda: update_weight())#

#def change_goal():

ui.run(reload=False, storage_secret='THIS_NEEDS_TO_BE_CHANGED')

