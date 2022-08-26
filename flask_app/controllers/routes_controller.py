from flask_app import app, bcrypt
from flask import render_template,redirect,request, session, flash
from flask_app.models import model_story

@app.route("/")
def landing_page():
    stories = model_story.Story.get_all_with_content_and_authors()
    return render_template("index.html", stories = stories)