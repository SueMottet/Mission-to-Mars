# use Flask to render a template, redirecting to another url, and creating a URL
from flask import Flask, render_template, redirect, url_for

#use PyMongo to interact with our Mongo database.
from flask_pymongo import PyMongo

# use the scraping code, we will convert from Jupyter notebook to Python.
import scraping

# set up Flask
app = Flask(__name__)

#Use flask_pymongo to set up connection through mLab
#app.config["MONGO_URI"] = os.environ.get('authentication')
#mongo = PyMongo(app)


# Use flask_pymongo to set up mongo connection
# tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL.
# This URI is saying that the app can reach Mongo through our localhost server, using port 27017, using a database named "mars_app".
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# define the route for the HTML page
# tells Flask what to display on the home page, index.html (index.html is the default HTML file we use to display content scraped
@app.route("/")
def index():
   # Uses PyMongo to find the "mars" collection in our database, created when we convert our Jupyter scraping code to Python Script.
   mars = mongo.db.mars.find_one()
   # tells Flask to return an HTML template using an index.html file and to use the mars collection
   return render_template("index.html", mars=mars)

#  set up our scraping route
# defines the route that Flask will be using
# will run the function beneath it.
@app.route("/scrape")
def scrape():
   # access the database, scrape new data using our scraping.py script, update the database, and return a message when successful.
   # assign a new variable that points to our Mongo database
   mars = mongo.db.mars

   # created a new variable to hold the newly scraped data
   mars_data = scraping.scrape_all()
   # update the database
   mars.update({}, mars_data, upsert=True)
   # use replace instead of update if update doesn't work -- replace_1 --replace_all
   
   # add a redirect after successfully scraping the data
   # navigates our page back to / where we can see the updated content.
   return redirect('/', code=302)

# code for Flask telling it to run
if __name__ == "__main__":
   app.run()