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

        def visible_change_weight():
            weight_card.set_visibility(True)

        def visible_change_playlist():
            playlist_card.set_visibility(True)


        def visible_change_goal():
            goal_card.set_visibility(True)

        ui.button('Change Weight', on_click= visible_change_weight)
        ui.button('Change Playlist', on_click=visible_change_playlist)
        ui.button('Change Goal', on_click=visible_change_goal)




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
