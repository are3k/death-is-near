import json
import requests
from pprint import pprint

api = "https://www.vegvesen.no/nvdb/api/v2/"

def hent_objecter(url):
	response = requests.get(api+url)
	return response

#url="vegobjekter.json"

url="vegobjekter.json/529Vegreferanse"
roadObjects = hent_objecter(url)
pprint(roadObjects.text)