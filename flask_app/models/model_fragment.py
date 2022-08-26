from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import app, DATABASE
from flask_app.models import model_user




class Fragment:
    def __init__( self , data ):
        self.id = data['id']
        self.content = data['content']
        self.segment = data['segment']
        self.author_id = data['author_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #C
    @classmethod
    def create_one_fragment(cls, data):
        query = "INSERT INTO fragments (content, segment, author_id) value (%(content)s, %(segment)s, %(author_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)


    #R
    @classmethod
    def get_one(cls, data):
        query = "Select * from fragments join users on fragments.author_id = users.id where fragments.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            flash("Something went wrong!")
        for result in results:
            
            user_data = {
                **result,
                "id" : result['users.id'],
                "created_at" : result["users.created_at"],
                "updated_at" : result["users.updated_at"]
            }
            result = cls(result)
            result.user = model_user.User(user_data)
        return result

    @classmethod
    def get_all(cls):
        query = "Select * from fragments join users on fragments.author_id = users.id"
        results = connectToMySQL(DATABASE).query_db(query)
        if not results:
            flash("Something went wrong!")
        all_fragments = []
        for result in results:
            
            user_data = {
                **result,
                "id" : result['users.id'],
                "created_at" : result["users.created_at"],
                "updated_at" : result["users.updated_at"]
            }
            result = cls(result)
            result.user = model_user.User(user_data)
            all_fragments.append(result)
        return all_fragments
    
    @classmethod
    def get_all_by_user_id(cls, data):
        query = "SELECT * FROM fragments where author_id = %(id)s"
        fragments = []
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return False
        for result in results:
            fragments.append(cls(result))
        return fragments

    #U
    @classmethod
    def update_one(cls, data):
        query = "UPDATE fragments SET content = %(content)s, segment = %(segment)s, author_id = %(author_id)s"
        return connectToMySQL(DATABASE).query_db(query, data)
    #D
    @classmethod
    def delete_one(cls, data):
        query = "DELETE from fragments WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate(fragment):
        is_valid = True
        if len(fragment["content"]) < 1:
            is_valid = False
            print("content length is the reason")
            flash("no readable text could be found on document. Please ensure file is a .txt", "err_fragment_content")
        if "segment" not in fragment:
            is_valid = False
            flash("you must select either a beginning, middle, or ending", "err_fragment_segment")
        if "user_id" not in session:
            is_valid = False
            flash("something went wrong when getting user information! Please enable cookies, logout, and log back in to retry submission", "err_fragment_author_id") 
        return is_valid

    @classmethod
    def create_relation(cls, data):
        query = "INSERT INTO stories_has_fragments (story_id, fragment_id) values ( %(story_id)s, %(fragment_id)s);" 
        return connectToMySQL(DATABASE).query_db(query, data)


    