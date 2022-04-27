from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from Scrapper import scrap_all, all_course
from mongodb import mongodbconnection
import logging


# Setting up logfile
logging.basicConfig(filename="flask_logs.log", format='%(asctime)s %(message)s', filemode='w', level=logging.INFO)

# MongoDB connection using mongo connection module
dbname = "iNeuron_scrapper"
collectionname = "course_collection"
dbcon = mongodbconnection(username='mongodb', password='mongodb')
ineuron_coll = dbcon.getCollection(dbName='iNeuron_scrapper', collectionName="course_collection")

# Function which automatically scraps all course data and saves to MongoDB server.
try:
    scraps = scrap_all()
    logging.info('Scrap Successful')
except Exception as e:
    logging.error('Error in Scraping check Scrapper.py', e)

# Connect to Flask
app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
@cross_origin()
def homepage():
    """Route to render the home page"""
    course_in = all_course()
    logging.info("List of Course names Generated")
    return render_template("index.html", course_in=course_in)


@app.route('/course', methods=['POST', 'GET'])
@cross_origin()
def result():
    """Route to render Results"""
    if request.method == 'POST':
        input_course = request.form['content'].replace("  ", " ")
        course_data = ineuron_coll.find_one({"Course_title": input_course}, {"_id": 0})
        logging.info("User input is taken and results Generated")
        return render_template("results.html", course_data=course_data)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run()
