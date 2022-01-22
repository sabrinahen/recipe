from flask import render_template, session,redirect, request
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route("/recipe/<int:id>")
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id" : id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_recipe.html", recipe=Recipe.getId(data), user=User.getId(user_data))

@app.route("/recipes/new")
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id":session['user_id']
    }
    return render_template("add_recipe.html", user=User.getId(data))

@app.route("/create/new", methods=["POST"])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "thirty_mins": int(request.form["thirty_mins"]),
        "date_made": request.form["date_made"],
        "user_id": session["user_id"]
    }
    Recipe.save(data)
    return redirect("/dashboard")

@app.route('/recipe/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/')
    data ={ 
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_recipe.html",recipe=Recipe.getId(data), user=User.getId(user_data))

@app.route('/update/recipe',methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "thirty_mins": int(request.form["thirty_mins"]),
        "date_made": request.form["date_made"],
    }
    Recipe.update(data)
    return redirect('/dashboard')

@app.route('/recipe/destroy/<int:id>')
def destroy_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id":id
    }
    Recipe.destroy(data)
    return redirect('/dashboard')
