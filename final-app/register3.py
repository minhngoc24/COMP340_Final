import psycopg
from psycopg.rows import dict_row
from dbinfo import *
from nicegui import ui, app

# Connect to database
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=flights user={DBUSER} password={DBPASS}")
cur = conn.cursor(row_factory=dict_row)

@ui.page('/')
def homepage():
    ui.html('''
    <style>
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(to bottom right, #f99aaa, #e0c3fc);
            color: #000000;
            font-size: 35px;
            text-align: center;
        }

        .header {
            background: linear-gradient(to bottom right, #a7bed3, #c1d3ff);
            backdrop-filter: blur(10px);
            border: #FAFABE;
            border-radius: 12px;
            padding: 1rem;
            margin: 1rem auto;
            width: 80%;
            max-width: 800px;
            color: black;
            font-family: fantasy;
        }

        .section-title {
            font-size: 1.5rem;
            color: #f0f0f0;
            margin-top: 2rem;
        }

        .card-tip {
            background: #761137;
            padding: 0.75rem;
            border-radius: 8px;
            margin: 1rem auto;
            width: 70%;
            max-width: 600px;
            border-left: 5px solid #ffffff88;
        }

        .btn-primary {
            background-color: #fdcfd1;
            color: #000000;
            padding: 0.5rem 1.2rem;
            border-radius: 8px;
            border: 1px solid #f9858b;
            margin: 0.3rem;
            font-weight: bold;
            transition: background 0.3s, transform 0.2s;
        }
        

        a {
            color: #ffffff;
            text-decoration: none;
            font-weight: bold;
            padding: 0.4rem 1rem;
            background-color: rgba(255, 255, 255, 0.15);
            border-radius: 8px;
            margin: 0.5rem;
            display: inline-block;
            transition: background 0.3s;
        }

        a:hover {
            background-color: rgba(255, 255, 255, 0.3);
        }
        
        
}
    </style>

    <div class="header">
        <h1>💪 Welcome to FitLife</h1>
        <p>Your personalized fitness journey starts here</p>
    </div>
    ''')

    ui.link("Login", '/login')
    ui.link("Logout", '/logout')

    username = app.storage.user.get('username', None)  # default if not logged in is None
    if username is not None:
        ui.label("You are logged in as user: " + username)
        ui.label("⬇ Please scroll down to choose what you want to do.")

        cur.execute('SELECT weight, playlist_genre, fitness_goal FROM USERS WHERE user_id = %s', (username,))
        row = cur.fetchone()
        weight = row['weight']
        playlist_genre = row['playlist_genre']
        fitness_goal = row['fitness_goal']

        playlist_result = ui.label('')
        result = ui.label('')
        goal_result = ui.label('')
        add_reviewGym_result = ui.label('')
        del_recipe_result = ui.label('')

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

        def visible_review_gym():
            add_reviewGym_card.set_visibility(True)

        def del_recipe_visibility():
            del_recipe_card.set_visibility(True)

        def visible_add_recipe():
            add_recipe_card.set_visibility(True)

        def get_my_recipes():
            def hide_my_table():
                recipe_card.set_visibility(False)

            cur.execute(
                "SELECT * FROM MakeRecipes natural join USERS natural join Recipes where MakeRecipes.user_id = %s",
                [username])
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

        ui.button('Change Weight', on_click=visible_change_weight, color='purple')
        ui.button('Change Playlist', on_click=visible_change_playlist, color='purple')
        ui.button('Change Goal', on_click=visible_change_goal, color='purple')
        ui.button('Search Recipes', on_click=get_recipes, color='green')
        ui.button('Add a New Recipe', on_click=visible_add_recipe, color='green')
        ui.button('Delete Recipe', on_click=del_recipe_visibility, color='green')
        ui.button('Get my recipes', on_click=get_my_recipes, color='green')
        ui.button('Find gyms within a radius', on_click=visible_find_gym, color='pink')
        ui.button('Find your Personal Trainer', on_click=visible_find_pt, color='pink')
        ui.button("Review Gyms", on_click=visible_review_gym, color='pink')


        def del_recipes():
            if del_recipe_box.value:
                cur.execute('DELETE FROM MakeRecipes where rid = %s and user_id = %s', [del_recipe_box.value, username])
                cur.execute('DELETE FROM Recipes where rid = %s', [del_recipe_box.value])
                conn.commit()
                del_recipe_result.text = f"Deleted recipe with ID: {del_recipe_box.value}"

                del_recipe_card.set_visibility(False)
            else:
                del_recipe_result.text = 'Please enter a valid playlist'

        with ui.card() as del_recipe_card:
            del_recipe_box = ui.input('Recipe ID:')
            ui.button('Confirm', on_click=del_recipes)
        del_recipe_card.set_visibility(False)

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
        def review_Gym():
            try:
                addr = addr_input.value
                ratings = ratings_input.value

                cur.execute("INSERT INTO reviewgym (user_id, address, rating) VALUES (%s, %s, %s)",
                            (username, addr, ratings))
                conn.commit()
                # Insert into recipes
                add_reviewGym_result.text = f"Review Gym '{addr}' added and marked as made!"
                add_reviewGym_card.set_visibility(False)

            except Exception as e:
                conn.rollback()
                add_reviewGym_result.text = f" Error: {str(e)}"

        with ui.card() as add_reviewGym_card:
            addr_input = ui.input('Address:')
            ratings_input = ui.input('Ratings:')
            ui.button('Confirm ratings', on_click=review_Gym)
        add_reviewGym_card.set_visibility(False)



        with ui.card() as findpt_card:
            def hide_my_table():
                findpt_card.set_visibility(False)

            get_user = ui.input('Enter user ID to look up PT:')
            pt_results = ui.column()

            pt_info = {}

            def find_pts():
                if get_user.value.isdigit():
                    cur.execute('''SELECT p.pt_id, p.name, p.experience, p.phone, f.Address FROM match m JOIN pt p ON m.pt_id = p.pt_id JOIN WorkInGym f ON p.pt_id = f.pt_id WHERE m.user_id = %s''', (get_user.value,))
                    pt_row = cur.fetchone()

                    cur.execute('SELECT fitness_goal FROM users WHERE user_id = %s', (get_user.value,))
                    user_row = cur.fetchone()

                    pt_results.clear()
                    with pt_results:
                        if pt_row and user_row:
                            pt_info['pt_id'] = pt_row['pt_id']  # store pt_id to use in submit
                            ui.label(f"{pt_row['name']} — {pt_row['experience']} yrs experience, {pt_row['phone']}")
                            ui.label(f"️ Works at: {pt_row['address']}")
                            ui.label(f"Helping you achieve your goal: {user_row['fitness_goal']}")

                            cur.execute(''' SELECT r.ratings, u.name AS reviewer FROM reviewpt r JOIN users u ON r.user_id = u.user_id WHERE r.pt_id = %s''', (pt_row['pt_id'],))
                            reviews = cur.fetchall()

                            if reviews:
                                ui.label("⭐ PT Reviews:")
                                for review in reviews:
                                    ui.label(f"- {review['reviewer']} rated {review['ratings']}/5")
                            else:
                                ui.label("No reviews yet for this PT.")
                        else:
                            ui.label("PT not found for this user.")

            ui.button('Show PT', on_click=find_pts)
            ui.button('Hide Table', on_click=hide_my_table)
        findpt_card.set_visibility(False)

        with ui.card() as findgym_card:
            def hide_my_table():
                findgym_card.set_visibility(False)

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
            ui.button('Hide Table', on_click=hide_my_table)

        findgym_card.set_visibility(False)


    else:
        ui.label("You are not logged in.")


@ui.page('/login')
def login(redirect_url='/'):
    ui.html('<h2 class="text-xl font-semibold text-indigo-700 mb-4">🔐 Login</h2>')

    def try_login():
        password = get_password_for_user(username_box.value)
        if password == password_box.value:
            app.storage.user['username'] = username_box.value
            ui.navigate.to(redirect_url)
        else:
            ui.notify('❌ Wrong username or password', color='negative')

    with ui.row().classes('items-center gap-4'):
        username_box = ui.input('Username:')
        password_box = ui.input('Password', password=True, password_toggle_button=True)
        ui.button('Log in', on_click=try_login, color= 'pink').classes(
            'bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-medium py-2 px-4 rounded hover:opacity-90 shadow-md'
        )


def get_password_for_user(user_id):
   cur.execute("SELECT age from USERS where user_id=%s", [user_id])
   row = cur.fetchone()
   return str(row['age'])  # return as a string to simulate a password


def get_weight_for_user(user_id):
   cur.execute("SELECT weight from USERS where user_id=%s", [user_id])
   row = cur.fetchone()
   return str(row['weight'])  # return as a string to simulate a password


@ui.page('/logout')
@ui.page('/logout')
def logout():
    app.storage.user.pop('username')
    ui.label("✅ You are now logged out.").classes("text-green-700 font-semibold mt-4")

    ui.link("🔙 Back to homepage", '/').classes(
        'inline-block mt-2 bg-indigo-500 text-white px-4 py-2 rounded hover:bg-indigo-600 transition'
    )

#def change_goal():

ui.run(reload=False, storage_secret='THIS_NEEDS_TO_BE_CHANGED', port = 8000)