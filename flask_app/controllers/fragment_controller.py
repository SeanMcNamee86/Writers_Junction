from flask_app import app, bcrypt
from flask import render_template,redirect,request, session, flash
from flask_app.models.model_fragment import Fragment
from flask_app.models import model_user, model_story

@app.route("/fragment/add_fragment/<int:id>")
def add_fragment_form(id):
    story = model_story.Story.get_one({ "id" : id})
    session['story_id'] = story.id
    return render_template("add_fragment.html", story = story)


@app.route("/fragment/add_fragment/<int:id>/create", methods = ["post"])
def add_fragment(id):
    content = request.files['content'].read()
    content.decode()
    fragment_data = {
        **request.form,
        "content" : content,
        "author_id" : session["user_id"]
    }
    if not Fragment.validate(fragment_data):
        return redirect(f"/fragment/add_fragment/{session['story_id']}")
    
    relation_data = {
        "story_id" : id,
        "fragment_id" : Fragment.create_one_fragment(fragment_data)
    }
    Fragment.create_relation(relation_data)
    if request.form['is_finished'] == 1:
        model_story.Story.finish_story({"id" : id})
    return redirect(f"/dashboard/{session['user_id']}")


@app.route("/fragments/browse")
def all_fragments():
    fragments = Fragment.get_all()
    return render_template("browse_fragments.html", fragments = fragments)