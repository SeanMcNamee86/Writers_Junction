from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import app, DATABASE



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data["password"]
        self.username = data["username"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE ID = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query, data)
        for user in results:
            user = cls(user) 
        return user

    @classmethod
    def check_matching_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if not result:
            return  False
        else:
            return True

    @classmethod
    def check_matching_username(cls, data):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if not result:
            return  False
        else:
            return True

    @classmethod
    def create_one(cls, data):
        query = "INSERT INTO users (first_name, last_name, username, email, password) values( %(first_name)s, %(last_name)s, %(username)s, %(email)s, %(pw)s);"
        connectToMySQL(DATABASE).query_db(query, data)
        return cls

    @staticmethod
    def validate_user( user ):
        is_valid = True
        if len(user["first_name"]) < 2:
            is_valid = False
            flash("invalid first name", "err_users_first_name")
        if len(user["last_name"]) < 2:
            is_valid = False
            flash("Invalid last name", "err_users_last_name")
        if len(user["username"]) < 5:
            is_valid = False
            flash("your username must be at least 5 characters in length!", "err_users_username")
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "err_users_email")
            is_valid = False
        if len(user["password"]) < 8 or user["pw"] != user["confirm_pw"]:
            flash("Invalid password or password fields do not match", "err_users_pw")
            is_valid = False
        if User.check_matching_email(user):
            flash("email already in use", "err_users_email")
            is_valid = False
        if User.check_matching_username(user):
            flash("username already in use", "err_users_username")
            is_valid = False
        if is_valid:
            flash("Registration success!", "err_users_none")
        return is_valid
    
    @classmethod
    def get_user_by_username(cls, data):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if not result:
            return False
        return cls(result[0])

    @staticmethod
    def validate_login( user ):
        is_valid = True

        if len(user["username"]) < 5:
            is_valid = False
            flash("your username must be at least 5 characters in length!", "err_users_username")
        return is_valid

