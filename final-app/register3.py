import psycopg
from psycopg.rows import dict_row
from dbinfo import *
from nicegui import ui, app

# --- Database connection ---
conn = psycopg.connect(f"host=localhost dbname=gymfinder user={DBUSER}")
cur = conn.cursor(row_factory=dict_row)

# ============================
#        HOMEPAGE
# ============================
@ui.page('/')
def homepage():
    ui.add_head_html("<title>FitLife</title>")
    ui.add_body_html("<style>body {background: linear-gradient(135deg, #e0eafc, #cfdef3);}</style>")

    # Welcome card
    with ui.card().classes("mx-auto mt-16 p-8 max-w-md text-center shadow-xl rounded-3xl bg-white"):
        ui.html("""
        <div>
          <div style="font-size:2rem;">💪</div>
          <h1 style="font-size:2rem; font-weight:600;">Welcome to <span style="color:#6366f1;">FitLife</span></h1>
          <p style="color:#555;">Your personalized fitness journey starts here</p>
        </div>
        """, sanitize=False)

    username = app.storage.user.get('username', None)

    if username:
        ui.label(f"You are logged in as user ID: {username}").classes("mt-4 text-gray-700")

        # === Recipes ===
        def get_recipes():
            cur.execute("SELECT * FROM recipes LIMIT 10;")
            rows = cur.fetchall()
            recipe_table.rows = rows
            recipe_card.visible = True

        with ui.card().props('bordered').classes("mt-4") as recipe_card:
            ui.label("📗 Recipes")
            recipe_table = ui.table(columns=[
                {'name': 'rid', 'label': 'Recipe ID', 'field': 'rid'},
                {'name': 'meal_name', 'label': 'Meal', 'field': 'meal_name'},
                {'name': 'description', 'label': 'Description', 'field': 'description'},
                {'name': 'calories', 'label': 'Calories', 'field': 'calories'},
                {'name': 'prep_time', 'label': 'Prep Time', 'field': 'prep_time'},
            ], rows=[])
        recipe_card.visible = False

        # === Find Gyms ===
        def find_gyms():
            cur.execute("SELECT gym_id, gym_name, location, rating, price FROM gyms LIMIT 10;")
            gyms = cur.fetchall()
            gym_table.rows = gyms
            gym_card.visible = True

        with ui.card().props('bordered').classes("mt-4") as gym_card:
            ui.label("🏋️ Nearby Gyms")
            gym_table = ui.table(columns=[
                {'name': 'gym_id', 'label': 'ID', 'field': 'gym_id'},
                {'name': 'gym_name', 'label': 'Name', 'field': 'gym_name'},
                {'name': 'location', 'label': 'Location', 'field': 'location'},
                {'name': 'rating', 'label': 'Rating', 'field': 'rating'},
                {'name': 'price', 'label': 'Price', 'field': 'price'}
            ], rows=[])
        gym_card.visible = False

        # === Find PT ===
        def find_pts():
            cur.execute("SELECT pt_id, name, experience, phone FROM pt LIMIT 10;")
            pts = cur.fetchall()
            pt_table.rows = pts
            pt_card.visible = True

        with ui.card().props('bordered').classes("mt-4") as pt_card:
            ui.label("💪 Personal Trainers")
            pt_table = ui.table(columns=[
                {'name': 'pt_id', 'label': 'ID', 'field': 'pt_id'},
                {'name': 'name', 'label': 'Name', 'field': 'name'},
                {'name': 'experience', 'label': 'Experience', 'field': 'experience'},
                {'name': 'phone', 'label': 'Phone', 'field': 'phone'}
            ], rows=[])
        pt_card.visible = False

        # === Smart Meal Plan ===
        def recommend_meals():
            cur.execute("""
                SELECT meal_name, description, calories FROM recipes
                WHERE calories < 400
                ORDER BY calories ASC LIMIT 5;
            """)
            meals = cur.fetchall()
            meal_table.rows = meals
            meal_card.visible = True

        with ui.card().props('bordered').classes("mt-4") as meal_card:
            ui.label("🍱 Smart Meal Plan")
            meal_table = ui.table(columns=[
                {'name': 'meal_name', 'label': 'Meal', 'field': 'meal_name'},
                {'name': 'description', 'label': 'Description', 'field': 'description'},
                {'name': 'calories', 'label': 'Calories', 'field': 'calories'}
            ], rows=[])
        meal_card.visible = False

        # === Review Gym ===
        def review_gym():
            cur.execute("SELECT * FROM reviewgym LIMIT 10;")
            reviews = cur.fetchall()
            review_gym_table.rows = reviews
            review_gym_card.visible = True

        with ui.card().props('bordered').classes("mt-4") as review_gym_card:
            ui.label("⭐ Gym Reviews")
            review_gym_table = ui.table(columns=[
                {'name': 'user_id', 'label': 'User', 'field': 'user_id'},
                {'name': 'gym_id', 'label': 'Gym', 'field': 'gym_id'},
                {'name': 'rating', 'label': 'Rating', 'field': 'rating'},
                {'name': 'comment', 'label': 'Comment', 'field': 'comment'}
            ], rows=[])
        review_gym_card.visible = False

        # === Review PT ===
        def review_pt():
            cur.execute("SELECT * FROM reviewpt LIMIT 10;")
            reviews = cur.fetchall()
            review_pt_table.rows = reviews
            review_pt_card.visible = True

        with ui.card().props('bordered').classes("mt-4") as review_pt_card:
            ui.label("💬 PT Reviews")
            review_pt_table = ui.table(columns=[
                {'name': 'user_id', 'label': 'User', 'field': 'user_id'},
                {'name': 'pt_id', 'label': 'PT', 'field': 'pt_id'},
                {'name': 'rating', 'label': 'Rating', 'field': 'rating'},
                {'name': 'comment', 'label': 'Comment', 'field': 'comment'}
            ], rows=[])
        review_pt_card.visible = False

        # === Buttons ===
        with ui.row().classes("mt-6 gap-2 justify-center"):
            ui.button("📗 View Recipes", on_click=get_recipes, color='green')
            ui.button("🏋️ Find Gyms", on_click=find_gyms, color='blue')
            ui.button("💬 Find PT", on_click=find_pts, color='purple')
            ui.button("🍱 Smart Meal Plan", on_click=recommend_meals, color='orange')
            ui.button("⭐ Gym Reviews", on_click=review_gym, color='pink')
            ui.button("💬 PT Reviews", on_click=review_pt, color='teal')

    else:
        ui.link("🔐 Login", '/login').classes("mt-6 text-indigo-600 underline")


# ============================
#        LOGIN PAGE
# ============================
@ui.page('/login')
def login(redirect_url='/'):
    ui.html('<h2 class="text-xl font-semibold text-indigo-700 mb-4">🔐 Login</h2>', sanitize=False)

    def try_login():
        try:
            password = get_password_for_user(username_box.value)
            if password == password_box.value:
                app.storage.user['username'] = username_box.value
                ui.navigate.to(redirect_url)
                ui.notify(f'✅ Logged in as user {username_box.value}', color='green')
            else:
                ui.notify('Wrong username or password', color='negative')
        except Exception as e:
            ui.notify(f"Database error: {e}", color='red')

    with ui.row().classes('items-center gap-4'):
        username_box = ui.input('User ID:')
        password_box = ui.input('Password (use your age):', password=True)
        ui.button('Log in', on_click=try_login, color='blue')


# ============================
#        LOGOUT PAGE
# ============================
@ui.page('/logout')
def logout():
    app.storage.user.pop('username', None)
    ui.label("You are now logged out.").classes("text-green-700 font-semibold mt-4")
    ui.link("🔙 Back to homepage", '/').classes(
        'inline-block mt-2 bg-indigo-500 text-white px-4 py-2 rounded hover:bg-indigo-600 transition'
    )


# ============================
#      HELPER FUNCTION
# ============================
def get_password_for_user(user_id):
    cur.execute("SELECT age FROM users WHERE user_id=%s", [user_id])
    row = cur.fetchone()
    return str(row['age']) if row else None


# ============================
#          RUN APP
# ============================
ui.run(reload=False, storage_secret='FITLIFE_SECRET', port=8000)
