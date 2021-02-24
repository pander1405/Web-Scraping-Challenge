from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# mongo = PyMongo(app)


mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template


@app.route('/scrape')