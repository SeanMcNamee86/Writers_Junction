from flask_app import app
from flask_app.controllers import fragment_controller, story_controller, user_controller, routes_controller



if __name__ == "__main__":
    app.run(debug=True)
