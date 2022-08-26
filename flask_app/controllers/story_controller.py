from flask_app import app, bcrypt
from flask import render_template,redirect,request, session, flash
from flask_app.models import model_story, model_fragment

@app.route("/story/new")
def new_fragment():
    return render_template("new_story.html")

@app.route("/story/new/create/", methods = ["post"])
def create_fragment():
    content = request.files['content'].read().decode()
    fragment_data = {
        **request.form,
        "content" : content,
        "author_id" : session["user_id"]
    }
    story_data = {
        "title" : request.form["story_title"],
        "founding_user_id" : session["user_id"]
    }
    if model_fragment.Fragment.validate(fragment_data) and model_story.Story.validate(story_data):
        
        flash("upload successful", "err_fragments_none")
        s_id = model_story.Story.create_one(story_data)
        relation_data = {
            "story_id" : s_id,
            "fragment_id" : model_fragment.Fragment.create_one_fragment(fragment_data) 
        }
        model_fragment.Fragment.create_relation(relation_data)
        if request.form["fragment_id_2"] != '':
            relation_data = {
                "story_id" : s_id,
                "fragment_id" : request.form["fragment_id_2"] 
            }
            model_fragment.Fragment.create_relation(relation_data)
    return redirect(f"/dashboard/{session['user_id']}")

@app.route("/stories/unfinished")
def list_stories():
    stories = model_story.Story.get_all_unfinished_stories()
    print(stories)
    return render_template("unfinished_stories.html", stories = stories)