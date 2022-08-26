from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app, DATABASE
from flask_app.models import model_fragment, model_user


class Story:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.founding_user_id = data['founding_user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create_one(cls, data):
        query = "INSERT INTO stories (founding_user_id, title, is_finished) values ( %(founding_user_id)s, %(title)s, 0 ) "
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "select * from stories join users on stories.founding_user_id = users.id WHERE stories.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        for result in results:
            user_data = {
                **result,
                "id" : result["users.id"],
                "created_at" : result["users.created_at"],
                "updated_at" : result["users.updated_at"]
            }
            story = cls(result)
            story.user = model_user.User(user_data)
            story.get_fragments_and_attach(story, {"id" : story.id})
        return story

    @classmethod
    def get_all_with_content_and_authors(cls):
        query = "select * from stories join users on stories.founding_user_id = users.id"
        results = connectToMySQL(DATABASE).query_db(query)
        stories = []
        for result in results:
            user_data = {
                **result,
                "id" : result["users.id"],
                "created_at" : result["users.created_at"],
                "updated_at" : result["users.updated_at"]
            }
            story = cls(result)
            story.user = model_user.User(user_data)
            story.get_fragments_and_attach(story, {"id" : story.id})
            stories.append(story)
        return stories

    @classmethod
    def get_fragments_and_attach(cls, story, data):
        query = "select* from stories join stories_has_fragments on stories.id = stories_has_fragments.story_id join fragments on stories_has_fragments.fragment_id = fragments.id join users on fragments.author_id = users.id where stories.id = %(id)s order by segment;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        story.fragments = []
        for result in results:
                fragment_data = {
                    **result,
                    "id" : result["fragments.id"],
                    "created_at" : result["fragments.created_at"],
                    "updated_at" : result["fragments.updated_at"]
                }
                user_data = {
                    **result,
                    "id" : result["users.id"],
                    "created_at" : result["users.created_at"],
                    "updated_at" : result["users.updated_at"]
                }
                fragment = model_fragment.Fragment(fragment_data)
                fragment.user = model_user.User(user_data)
                story.fragments.append(fragment)
        print(story.fragments)
        return story

    @classmethod
    def update_one(cls, data):
        query = "UPDATE stories SET where id = %(id)s"
        connectToMySQL(DATABASE).query_db(query, data)
        return cls

    @classmethod
    def delete_one(cls, data):
        query = "DELETE from stories where id = %(id)s"
        connectToMySQL(DATABASE).query_db(query, data)
        return cls

    @classmethod
    def get_all_stories_with_authors(cls):
        query = "SELECT * FROM stories JOIN users ON stories.author_id = users.id"
        results = connectToMySQL(DATABASE).query_db(query)
        all_stories = []
        for result in results:
            user_data = {
                **result,
                "id" : result["users.id"],
                "created_at" : result['users.created_at'],
                "updated_at" : result['users.updated_at']
            }
            result = cls(result)
            result.user = model_user.User(user_data)
            all_stories.append(result)
            data = {
                "id" :result.id
            }
        return all_stories

    @classmethod
    def get_all_unfinished_stories(cls):
        query = "SELECT * FROM stories JOIN users on stories.founding_user_id = users.id  WHERE is_finished = '0' "
        all_results = []
        results =  connectToMySQL(DATABASE).query_db(query)
        for result in results:
            story = cls(result)
            user_data = {
                **result,
                "id" : result["users.id"],
                "created_at" : result['users.created_at'],
                "updated_at" : result['users.updated_at']
            }
            story.user = model_user.User(user_data)
            story.get_fragments_and_attach(story, { "id" : story.id})
            all_results.append(story)
        return all_results

    @classmethod
    def finish_story(data):
        query = "UPDATE stories set is_finished = 1 where id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query)

    @staticmethod
    def validate(story):
        is_valid = True
        if len(story['title']) < 3:
            flash("Please enter a title that is at least 3 characters long", "err_story_title")
            is_valid = False
        return is_valid


