from flask import Flask, jsonify, abort, make_response, request, url_for, g
import config
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timezone, datetime
from flask_httpauth import HTTPBasicAuth
import json
import bson
from pprint import pprint

auth = HTTPBasicAuth()



client = MongoClient('localhost', 27017)
db = client[config.db_name]
books = db[config.book_collection]

app = Flask(__name__)

#custom error handler to create own error response 
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': 'Not Found'}), 404)


#custom error handler to create own error response 
@app.errorhandler(400)
def invalid_req(error):
    return make_response(jsonify({'Error': 'Invalid Request'}), 400)

#custom error handler to create own error response
@auth.error_handler
def unauthorized():
    # return error
    return make_response(jsonify({'error': 'Unauthorized Access'}), 403)

#index route that currently does nothing and just shows message
@app.route('/')
def index():
	return "Welcome to API!"


@app.route('/book_keeper/api/user', methods = ['POST'])
def register():

	#get username and password user gives
	username = request.json.get('username')
	password = request.json.get('password')

	#if data missing from json, return error
	if not request.json or username is None or password is None:
		abort(400)

	#if user already exists, return error 
	if books.find_one({"username" : username}) is not None:
		abort(400)

	#create password hash for users password
	hash_password = generate_password_hash(password)

	#user id is based on unix timestamp
	u_id = int(datetime.now().timestamp() * 1000)

	#insert user into db with no books
	books.insert_one({"_id" : u_id, "username" : username, "password" : hash_password, "books" : []})

	#return json with username that was registered, 201 success code, and header pointing to get_user
	return jsonify({ 'username': username }), 201, {'Location': url_for('get_user', username = username, _external = True)}


#get user based on username 
@app.route('/book_keeper/api/user/<string:username>')
def get_user(username):
	#look up based on username 
    user = books.find_one({"username" : username})

    #if no user, return error 
    if not user:
        abort(404)

    #create response to return after request
    user_response = {'username': user['username'], 'id': user['_id'], 'total_books': len(user['books']) }

    #return json with username
    return jsonify(user_response)


#check for valid auth password
@auth.verify_password
def verify_password(username, password):
	#look up user
    user = books.find_one({"username" : username})

    #if user not found or password doesn't match unhashed pass, return false
    if not user or not check_password_hash(user['password'], password):
        return False

    #return true and set g.user to username 
    g.user = user['username']
    return True

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

#add a book to a user's list of books
@app.route('/book_keeper/api/user/books', methods = ['POST'])
@auth.login_required
def post_book():
	#get key values from json
	name = request.json.get('name')
	author = request.json.get('author')
	pages = request.json.get('pages')
	completed = request.json.get('completed')

	#get authenticated users username
	username = request.authorization.username

	#if not json or any of values none, return error
	if not request.json or name is None or author is None or pages is None or completed is None:
		abort(400)

	#get json passed by user and add a unique id to book
	book = request.json
	book['book_id'] = str(bson.objectid.ObjectId())

	#insert into users books list 
	books.find_one_and_update({"username": username}, {"$push": {"books": book}}, upsert = True)
	return jsonify({'book': book}), 201


@app.route('/book_keeper/api/user/book/<string:book_id>', methods = ['PUT'])
@auth.login_required
def update_book(book_id):

	#get json from request
	book_mod = request.json

	#checks on json, if not json error
	if not request.json:
	    abort(400)
	#check for elements in the json and check for data type, return error 
	if 'name' in book_mod and type(book_mod['name']) is not str:
	    abort(400)
	if 'author' in book_mod and type(book_mod['author']) is not str:
	    abort(400)
	if 'pages' in book_mod and type(book_mod['pages']) is not int:
	    abort(400)
	if 'completed' in book_mod and type(book_mod['completed']) is not bool:
	    abort(400)

	#get username from request
	username = request.authorization.username

	#lookup user and book id
	books_lookup = books.find_one({"$and": [{"username": username}, {"books.book_id" : book_id}]}, {"books.$" : 1})

	#if nothing found, return error
	if books_lookup is None:
		abort(404)

	#getting actual book information 
	book = books_lookup['books'][0]

	#setting the book info based on json, if no new info, keep original value
	book['name'] = book_mod.get('name', book['name'])
	book['author'] = book_mod.get('author', book['author'])
	book['pages'] = book_mod.get('pages', book['pages'])
	book['completed'] = book_mod.get('completed', book['completed'])

	#find book by id and update with new json
	put = books.find_one_and_update({"$and": [{"username": username}, {"books.book_id" : book_id}]}, {"$set": {"books.$": book}}, upsert = True)

	#return book that was updated
	return jsonify({'book': book})



#route to delete an authenticated users book based on ID
@app.route('/book_keeper/api/user/book/<string:book_id>', methods = ['DELETE'])
@auth.login_required
def delete_book(book_id):
	#look up desired book to see if it even exists so we can delete 
	books_lookup = books.find_one({"$and": [{"username": request.authorization.username}, {"books.book_id" : book_id}]}, {"books.$" : 1})

	#if it doesn't exist, return error
	if books_lookup is None:
		abort(404)

	#does exist so find that specific book and delete the subdocument pertaining to doc 
	delete = books.find_one_and_update({"username": request.authorization.username},{"$pull":{"books": {"book_id" : book_id}}}, upsert=False)
	#return validation to user
	return jsonify({'Delete': 'Success!'})


#route to handle get requests for getting all books for a user
@app.route('/book_keeper/api/user/<string:username>/books', methods = ['GET'])
def get_books(username):

	#lookup user in DB based on username 
	user_lookup = books.find_one({'username' : username})

	if user_lookup is None:
		abort(404)

	#get all user books
	user_books = user_lookup['books']

	#convert to json response format and return 
	return jsonify({"books": user_books})


#route to handle getting single book based on book id 
@app.route('/book_keeper/api/user/book/<string:book_id>', methods = ['GET'])
@auth.login_required
def get_book(book_id):

	#lookup to get authenticated users books
	books_lookup = books.find_one({"$and": [{"username": request.authorization.username}, {"books.book_id" : book_id}]}, {"books.$" : 1})

	#no books found, return resource not found error 
	if books_lookup is None:
		abort(404)

	#return book found 
	return jsonify({"book": books_lookup['books'][0]})

#route to handle returning all user books that are completed
@app.route('/book_keeper/api/user/books/completed/', methods = ['GET'])
@auth.login_required
def get_completed():

	#find user and get their books
	books_lookup = books.find_one({"username": request.authorization.username}, {"books": 1})

	#if not found, return error
	if books_lookup is None:
		abort(404)

	#otherwise return json of books where book is completed
	return jsonify({'books': [book for book in books_lookup['books'] if book['completed'] == True]})


	
if __name__ == '__main__':
    app.secret_key = config.secret_key

    app.run(debug=True)