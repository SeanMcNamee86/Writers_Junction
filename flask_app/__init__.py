from flask import Flask
from flask_bcrypt import Bcrypt

DATABASE = "story_roulette_db"

app = Flask(__name__)

app.secret_key = "af5901321eg124afbc0c87ce1"

bcrypt = Bcrypt(app)
