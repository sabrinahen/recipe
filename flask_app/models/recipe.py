from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Recipe:
    db = "recipe_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.thirty_mins = data["thirty_mins"]
        self.instructions = data["instructions"]
        self.date_made = data["date_made"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def getAll(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, thirty_mins, instructions, date_made) VALUES (%(name)s, %(description)s, %(thirty_mins)s, %(instructions)s, %(date_made)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def getId(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, thirty_mins=%(thirty_mins)s, instructions=%(instructions)s, date_made=%(date_made)s, updated_at=%(updated_at)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query  = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 2:
            flash("Name must be at least 2 characters")
            is_valid= False
        if len(recipe['description']) < 2:
            flash("Description must be at least 5 characters")
            is_valid= False
        if len(recipe['instructions']) < 8:
            flash("Instructions must be at least 5 characters")
            is_valid= False
        if recipe['date_made'] == "":
            is_valid = False
        return is_valid
