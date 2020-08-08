from flask import Flask, render_template, redirect
import pymongo
from scrape_mars import scrape
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd


#Database setup
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db=client.mars_db
collection=db.marstable

#Flask setup
app = Flask(__name__)


@app.route("/")
def home():

    #extract documents from a pymongo collection
    cursor = collection.find_one()
    #feed documents to the html file
    return render_template("index.html", scraped_info=cursor)

##@app.route("/scrape")
##def scrape():
##
##    scraped_data = scrape()
##    
##    #delete existing document in a collection
##    collection.delete_many({})
##    #insert scraped data into collection
##    collection.insert_one(scraped_data)
##    
##    # return user back to the homepage
##    return redirect("/")
@app.route('/scrape', methods=['GET'])
def data_scrape():
    scraped=scrape()
    collection.delete_many({})
    collection.insert_one(scraped)
    print(scraped)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=False, port=5002)
