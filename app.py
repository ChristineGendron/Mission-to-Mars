


from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection

app.config['MONGO_URI'] = "mongodb://localhost:27017/mars_app"

mongo = PyMongo(app)

# set up routes 

@app.route('/')

#tells what to display when we're on the home page & links links visual to the code

def index():
    
    #use pmongo to find the mars mongo db
    
    mars = mongo.db.mars.find_one()
    
    return render_template('index.html', mars=mars) #we will create this template later



#add scraping route, which will be a button

@app.route('/scrape')

def scrape():
    
    #assign variable for mongo database
    mars = mongo.db.mars
    
    #assign variable to the scraped data
    mars_data = scraping.scrape_all()
    
    #update the database with scraped data (upsert tells it to insert if it doesn't match existing data)
    mars.update_one({}, {'$set':mars_data}, upsert=True)
    
    #sends our page back to default
    return redirect('/', code=302)



if __name__ == "__main__":
   app.run()

