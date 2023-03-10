from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# model the class after the friend table from our database
class Users:
    DB = "users_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
            # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.DB).query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user) )
        return users
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    @classmethod
    def save(cls, data ):
        query = """
                INSERT into users 
                (first_name, last_name, email, created_at, updated_at) 
                VALUES 
                ( %(first_name)s , %(last_name)s , %(email)s , NOW() , NOW() )
        
        """
        # data is a dictionary that will be passed into the save method from server.py
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result


    @classmethod
    def update(cls,data):
        query = """
                UPDATE users
                set first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s
                WHERE id = %(id)s;
        """
                #Semicolon not neeed, only best practice
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @classmethod
    def delete(cls, data): #double check on this delete(id)
        query = """
                DELETE FROM users
                WHERE id = %(id)s;
        
        """
        # data= {"id":id }
        
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @staticmethod
    def validated_user(form_data):
        is_valid = True
        if len(form_data["first_name"]) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(form_data["last_name"]) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(form_data["email"]):
            flash ("Invalid email address.")
            is_valid = False
        
        return is_valid


        # return connectToMySQL('first_flask').query_db( query, data )

