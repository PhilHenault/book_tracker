# Book_Keeper
Book_Tracker is an API developed using Python and the Flask microframework. Authenticated users can add books to their account, modify their status, retrieve information about them, and remove them. 

## Authentication

Book_Tracker makes use of Basic Authentication. To access most resources, a user must pass a username and password with the request. 

#### Register an Account
This request allows a user to register an account in order to make authenticated requests to the API. 
&NewLine;
```sh
POST http://localhost:5000/book_tracker/api/user
```
```json
    {
        "username" : "sample_username",
        "password" : "sample_password"
    }
```
In the request, pass along a JSON with the requested username and password. 

##### Example
```sh
curl -i -X POST -H "Content-Type: application/json" -d '{"username":"sample_username","password":"sample_password"}' http://localhost:5000/book_tracker/api/user
```

#### Response
```json
    {
        "username": "sample_username"
    }
```

## Authenticated Requests

##### Add a Book
This request allows an authenticated user to add a book to their account. 
&NewLine;
```sh
POST http://localhost:5000/book_tracker/api/user/books
```
```json
    {
        "name" : "sample_name",
        "author" : "sample_author",
        "pages" : "sample_pages (int)",
        "completed" : "sample_completed (bool)"
    }
```

Pass along a JSON of book details to add the book to a user's collection. 
##### Example
```sh
curl -i -u username:password -X POST -H "Content-Type: application/json" -d '{'name:"sample_name",'author':'sample_author', 'pages': sample_pages, 'completed' : sample_completed}' http://localhost:5000/book_tracker/api/user/books
```
#### Response
```json
    {
        "book": {
            "author": "sample author",
            "book_id": "5c6eafb3808da62203f81828",
            "completed": false,
            "name": "sample book",
            "pages": 250
        }
    }
```
&NewLine;
##### Update a Book
This request allows an authenticated user to update an existing book in their collection. 
&NewLine;
```sh
PUT http://localhost:5000/book_tracker/api/user/book/<string:book_id>
```

Authenticated user's must pass a unique book ID to update a book. This book ID can be found through **Getting Completed Books**, **Getting Currently Reading**, or **Getting a User's Books**

```json
    {
        "name" : "sample_name",
        "author" : "sample_author",
        "pages" : "sample_pages (int)",
        "completed" : "sample_completed (bool)"
    }
```

Pass along a JSON of book details to update the existing book with new information.  
##### Example
```sh
curl -i -u username:password -X PUT -H "Content-Type: application/json" -d '{'name:"sample_name",'author':'sample_author', 'pages': sample_pages, 'completed' : sample_completed}' http://localhost:5000/book_tracker/api/user/book/book_id
```

#### Response
```json
    {
        "book": {
            "author": "sample author",
            "book_id": "5c6eafb3808da62203f81828",
            "completed": false,
            "name": "Testing Update",
            "pages": 250
        }
    }
```
&NewLine;
##### Delete a Book
This request allows an authenticated user to delete an existing book from their collection. 
&NewLine;
```sh
DELETE http://localhost:5000/book_tracker/api/user/book/<string:book_id>
```

Authenticated user's must pass a unique book ID to delete a book. This book ID can be found through **Getting Completed Books**, **Getting Currently Reading**, or **Getting a User's Books**

##### Example
```sh
curl -i -u username:password -X DELETE -H "Content-Type: application/json"  http://localhost:5000/book_tracker/api/user/book/book_id
```

#### Response
```json
    {
        "Delete": "Success!"
    }
```

&NewLine;
##### Get a Specific Book
This request allows an authenticated user to retrieve a book from their collection. 
&NewLine;
```sh
GET http://localhost:5000/book_tracker/api/user/book/<string:book_id>
```

Authenticated user's must pass a unique book ID to retrieve a specific book. This book ID can be found through **Getting Completed Books**, **Getting Currently Reading**, or **Getting a User's Books**

##### Example
```sh
curl -i -u username:password -X GET -H "Content-Type: application/json"  http://localhost:5000/book_tracker/api/user/book/book_id
```

#### Response
```json
    {
        "book": {
            "author": "sample author",
            "book_id": "5c6eb1d6808da62203f81829",
            "completed": false,
            "name": "sample book",
            "pages": 250
        }
    }
```
&NewLine;
##### Get a User's Completed Books
This request allows an authenticated user to retrieve books that are marked as completed. 
&NewLine;
```sh
GET http://localhost:5000/book_tracker/api/user/books/completed
```

##### Example
```sh
curl -i -u username:password -X GET -H "Content-Type: application/json"  http://localhost:5000/book_tracker/api/user/books/completed
```

#### Response
```json
{
    "books": [
        {
            "book_id": "123",
            "author": "Phil Knight",
            "completed": true,
            "name": "Shoe Dog: A Memoir by the Creator of Nike",
            "pages": 400
        },
        {
            "book_id": "456",
            "author": "Ben Horowitz",
            "completed": true,
            "name": "The Hard Thing About Hard Things: Building a Business When There Are No Easy Answers",
            "pages": 304
        }
    ]
}
```
&NewLine;
##### Get a User's In-Progress Books
This request allows an authenticated user to retrieve books that are marked as being read. 
&NewLine;
```sh
GET http://localhost:5000/book_tracker/api/user/books/reading
```

##### Example
```sh
curl -i -u username:password -X GET -H "Content-Type: application/json"  http://localhost:5000/book_tracker/api/user/books/reading
```

#### Response
```json
{
    "books": [
        {
            "_id": "234",
            "author": "Ben Horowitz",
            "completed": false,
            "name": "The Hard Thing About Hard Things: Building a Business When There Are No Easy Answers",
            "pages": 304
        },
        {
            "author": "sample author",
            "book_id": "5c6eb1d6808da62203f81829",
            "completed": false,
            "name": "sample book",
            "pages": 250
        }
    ]
}
```
## Unauthenticated Requests
&NewLine;
##### Get a User
This request allows an unauthenticated user to get information about a registered user.
&NewLine;
```sh
GET http://localhost:5000/book_tracker/api/user/<string:username>
```

##### Example
```sh
curl -i -X GET -H "Content-Type: application/json"  http://localhost:5000/book_tracker/api/user/username_string
```

#### Response
```json
    {
        "id": 1550757663137,
        "total_books": 3,
        "username": "sample_username"
    }
```
&NewLine;
##### Get a User's Books
This request allows an unauthenticated user to get the books of a user.
&NewLine;
```sh
GET http://localhost:5000/book_tracker/api/user/<string:username>/books
```

##### Example
```sh
curl -i -X GET -H "Content-Type: application/json"  http://localhost:5000/book_tracker/api/user/username_string/books
```

#### Response
```json
    {
        "books": [
            {
                "author": "Phil Knight",
                "book_id": "123",
                "completed": true,
                "name": "Shoe Dog: A Memoir by the Creator of Nike",
                "pages": 400
            },
            {
                "author": "Ben Horowitz",
                "book_id": "456",
                "completed": true,
                "name": "The Hard Thing About Hard Things: Building a Business When There Are No Easy Answers",
                "pages": 304
            },
            {
                "author": "Ben Horowitz",
                "book_id": "234",
                "completed": false,
                "name": "The Hard Thing About Hard Things: Building a Business When There Are No Easy Answers",
                "pages": 304
            }
        ]
    }
```
