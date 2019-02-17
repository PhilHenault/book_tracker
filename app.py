from flask import Flask, jsonify, abort, make_response
import config
from pymongo import MongoClient
from bson.json_util import loads
import json
from bson import json_util
import json

client = MongoClient('localhost', 27017)
db = client[config.db_name]
books = db[config.book_collection]

app = Flask(__name__)

#index route that currently does nothing and just shows message
@app.route('/')
def index():
	return "Welcome to API!"

#handles the conversion of objectIDs to strings
def objectId_handler(results, is_list = True):
	#if list, iterate through and fix all
	if is_list:
		for res in results:
			#convert ID to string
			res["_id"] = str(res["_id"])
		return results
	#not a list, convert object ID to strnig
	else:
		results["_id"] = str(results["_id"])
		return results

	
#custom error handler to create own error response 
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': 'Not Found'}), 404)


#custom error handler to create own error response 
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'Error': 'Invalid Request'}), 400)


#route to handle get requests for getting all books
@app.route('/book_keeper/api/books', methods = ['GET'])
def get_books():
	#query the collection and handle conversion of IDs to strings
	books_response = objectId_handler(list(books.find({})))

	#convert to json response format and return 
	return jsonify({"books": books_response})


#route to handle getting single book based on book id
@app.route('/book_keeper/api/book/<book_id>', methods = ['GET'])
def get_book(book_id):

	#if book id is not a numeric value return error
	try:
		book_id = int(book_id)
	except:
		abort(400)


	#if book id is numeric, do lookup for it
	book = books.find_one({"book_id" : int(book_id)})
	
	#no books found, return resource not found error 
	if book is None:
		abort(404)

	#restructure data to remove "_id"
	# book_response = restructure_data(book, False)
	#convert to json response format and return 
	return jsonify({"book": book})
		

if __name__ == '__main__':
    app.secret_key = config.secret_key

    app.run(debug=True)