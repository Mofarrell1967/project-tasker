import os
from flask import Flask
from flask_pymongo import PyMongo


@app.route('/')
def get_projects():
    return render_template("projects.html", projects=mongo.db.projects.find())

    