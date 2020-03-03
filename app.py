from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars_data

@app.route("/")
def index():
    mars_data = db.mars_data.find_one()
    return render_template("index.html", mars_data = mars_data)
    

@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape() 
    db.mars_data.insert_one(mars_data)
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)