from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars.ipynb

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    info = mongo.db.articles.find_one()
    return render_template("index.html", mars = info)


@app.route("/scrape")
def scraper():
    mars_data = ScrippyScrape.scrape()
    mongo.db.articles.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)