# Script to let us register students.

import psycopg
from aext_shared import user_id
from psycopg.rows import dict_row
from xarray.core.weighted import Weighted

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

@ui.page('/')
def homepage():
    ui.label("Welcome to the homepage!")
    ui.link("Login", '/login')

    username = app.storage.user.get('username', None)  # default if not logged in is None
    if username is not None:
        ui.label("You are logged in as user: " + username)

        cur.execute('SELECT weight FROM USERS WHERE user_id = %s', (username,))
        weight = cur.fetchone()['weight']
        current_weight_label = ui.label(f'Current weight is: {weight}')

        user_box = ui.input('User ID:')
        newweight_box = ui.input('New Weight:')
        result = ui.label('')

        def update_weight():
            if user_box.value.isdigit() and newweight_box.value:
                cur.execute('UPDATE USERS SET weight = %s WHERE user_id = %s',
                            (newweight_box.value, user_box.value))
                conn.commit()
                current_weight_label.text = f"Current weight is: {newweight_box.value}"
                result.text = f"New weight is: {newweight_box.value}"
            else:
                result.text = 'Please enter a valid user ID and weight.'

        ui.button('Change Weight', on_click=update_weight)

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
    ui.label("Use a user_id numbfer for username and the grad year for password.")
    with ui.row().classes('items-center'):
        username_box = ui.input('Username:')
        password_box = ui.input('Password', password=True, password_toggle_button=True)
        ui.button('Log in', on_click=try_login)





def get_password_for_user(user_id):
    cur.execute("SELECT age from USERS where user_id=%s", [user_id])
    row = cur.fetchone()
    return str(row['age'])  # return as a string to simulate a password


@ui.page('/logout')
def logout():
    app.storage.user.pop('username')
    ui.label("You are now logged out.")
    ui.link("Back to homepage", '/')
    #ui.button('Register!', on_click=lambda: update_weight())


#def change_goal():



ui.run(reload=False, storage_secret='THIS_NEEDS_TO_BE_CHANGED')
