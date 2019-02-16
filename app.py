from flask import Flask
import config
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client[config.db_name]
books = db[config.book_collection]

app = Flask(__name__)

@app.route('/')
def index():
	return "Welcome to API!"

if __name__ == '__main__':
    app.secret_key = config.secret_key

    app.run(debug=True)