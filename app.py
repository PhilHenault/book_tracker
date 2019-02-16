from flask import Flask, jsonify
import config
from pymongo import MongoClient
from bson.json_util import loads
import json

client = MongoClient('localhost', 27017)
db = client[config.db_name]
books = db[config.book_collection]

app = Flask(__name__)

#index route that currently does nothing and just shows message
@app.route('/')
def index():
	return "Welcome to API!"


#takes in a list and restructures data by removing the "_id" key to make the response more readable
def restructure_data(data_list):
	to_return = []
	#iterate through 
	for item in data_list:
		#delete "_id" for each
		del item["_id"]
		#re add the element in order to return it 
		to_return.append(item)
	return to_return


#route to handle get requests for getting all books
@app.route('/book-keeper/api/books', methods = ['GET'])
def get_books():
	#query the collection and restructure books
	books_response = restructure_data(list(books.find({})))
	#convert to json response format and return 
	return jsonify({"books": books_response})




if __name__ == '__main__':
    app.secret_key = config.secret_key

    app.run(debug=True)