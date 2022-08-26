
from flask_app import app, bcrypt
from flask import render_template,redirect,request, session, flash
from flask_app.models.model_user import User
from flask_app.models import model_fragment




@app.route("/create")
def create_new():
    return render_template("create.html")



@app.route("/registration")
def registration():
    return render_template("registration_page.html")

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    data = {
        **request.form
    }
    data["pw"] = bcrypt.generate_password_hash(data["pw"])
    user = User.create_one(data)
    return redirect('/')

@app.route("/dashboard/<int:id>")
def dashboard(id):
    if "user_id" not in session:
        flash("something went wrong with user id request, please enable cookies and log back in")
        return redirect("/")
    fragments = model_fragment.Fragment.get_all_by_user_id({"id" : id})
    return render_template("dashboard.html", fragments = fragments)

@app.route("/login_page")
def login_page():
    return render_template("login_page.html")

@app.route("/login", methods = ["post"])
def login():
    data = {
        "username" : request.form["username"],
        }
    if not User.validate_login(data):
        return redirect("/login_page")
    user_in_db = User.get_user_by_username(data)
    if not user_in_db:
        flash("no matching username found", "err_users_username")
        return redirect("/login_page")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password combination", "err_users_username")
        return redirect('/login_page')
    session["user_id"] = user_in_db.id
    session["username"] = user_in_db.username
    return redirect("/")





@app.route("/logout")
def loogout():
    del session["user_id"]
    return redirect("/")

