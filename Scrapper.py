import logging
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import json
from mongodb import mongodbconnection

### Setting up Logging file ###
logging.basicConfig(filename="flask_logs.log",format='%(asctime)s %(message)s',filemode='w',level = logging.DEBUG)

### Function to Scrap all course title from iNeuron website ###
def all_course():
    try:
        ineuron_url = 'https://courses.ineuron.ai/'
        uClient = uReq(ineuron_url)
        ineuron_page = uClient.read()
        uClient.close()
        ineuron_html = bs(ineuron_page, 'html.parser')
        course_data = json.loads(ineuron_html.find('script', {"id": "__NEXT_DATA__"}).get_text())
        all_courses = course_data['props']['pageProps']['initialState']['init']['courses']
        course_namelist = list(all_courses.keys())
        return course_namelist
    except:
        logging.error('Error in scraping at all_course()')

### Function to Scrap one Course details from iNeuron website ###
def get_course(coursename):
    ineuron_url = 'https://courses.ineuron.ai/'
    uClient = uReq(ineuron_url + str(coursename).replace(" ", "-"))
    course_page = uClient.read()
    uClient.close()
    ineuron_html = bs(course_page, 'html.parser')
    course_data1 = json.loads(ineuron_html.find('script', {"id": "__NEXT_DATA__"}).get_text())
    logging.info('Course data saved as JSON format')
    all_dict = {}
    #list = []
    try:
        try:
            all_data = course_data1["props"]["pageProps"]
        except:
            all_data = 'No page'
        try:
            page_data = all_data['data']
        except:
            page_data = 'No data'
        try:
            detailed_data = page_data['details']
        except:
            detailed_data = 'No details'
        try:
            meta_data = page_data['meta']
        except:
            meta_data = 'No meta_data'
        try:
            curriculum_data = meta_data['curriculum']
        except:
            curriculum_data = 'No curriculum_data'
        try:
            overview_data = meta_data['overview']
        except:
            overview_data = 'No overview_data'
#####   Building a Course Dictionary
        try:
            pricing_inr = detailed_data['pricing']['IN']
        except:
            pricing_inr = 'NULL'
        try:
            course_name = page_data['title']
        except:
            course_name = 'Name NA'
        try:
            description = detailed_data['description']
        except:
            description = "NULL"
        try:
            language = overview_data['language']
        except:
            language = 'NULL'
        try:
            req = overview_data['requirements']
        except:
            req = 'NULL'
        try:
            learn = overview_data['learn']
        except:
            learn = 'NULL'
        curriculum = []
        try:
            for i in curriculum_data:
                curriculum.append(curriculum_data[i]["title"])
                ### Saving all the data in dictionary format ###
            all_dict = {"Course_title": course_name, "Description": description,
                 "Language": language, "Pricing": pricing_inr,
                 "Curriculum_data": curriculum, "Learn": learn,
                 "Requirements": req}
            logging.info('dict is created')
        except:
            curriculum.append('NULL')
        return all_dict
    except:
        logging.error('Error in Scrapping at get_course()')

### Function which gets all the course data and saves it in mongodb ###
def scrap_all():
    #mongodb module to do mongodb operations
    dbcon = mongodbconnection(username = 'mongodb', password = 'mongodb')
    db_collection = dbcon.getCollection("iNeuron_scrapper","course_collection")
    try:
        if dbcon.isCollectionPresent("iNeuron_scrapper","course_collection"):
            pass
        else:
            final_list = []
            list_courses = all_course()
            for i in list_courses:
                final_list.append(get_course(i))
            db_collection.insert_many(final_list)
    except Exception as e:
            logging.error("error in DB insertion",e)





