# Python Comic API
## Table of Content
1. [Introduction](#introduction)
2. [Installation](#install)
2. [Live example](#example)
3. [API Docs](#api_docs)



## Introduction <a name="introduction"></a>
This is an API developed with Python using Flask and JWT in order to have secure routes.

## Installation <a name="install"></a>
  1. Clone this repository
  2. Run ``` pip install -r requirements.txt ``` in the root directory
  3. Run ```python myapp.py```

## Live Example <a name="example"></a>
There is a Live example for this API deployed in Heroku. In order to start you have to make a request to the following URI 
```
https://python-comic-api.herokuapp.com/
```
## API Docs <a name="api_docs"></a>
The API routes are protected with JWT, so in order to use the routes, you need to login, to do this send a GET request with Basic Auth (see image)
![alt text](http://res.cloudinary.com/jrleon90/image/upload/v1528004591/login_comic_api.png "Postman example")
  The request has to be made to the following URI
  ```
 GET https://python-comic-api.herokuapp.com/login
  ```
  Once the request has been made with a valid login information, it returns a token that needs to be save in order to made every request.
  
1. **GET COMICS**

Send GET request to
  ```
 GET https://python-comic-api.herokuapp.com/comics
  ```
Since the routes are protected, the user needs to send the token in the header of the request with the key name "x-access-token" (see image)
![alt text](http://res.cloudinary.com/jrleon90/image/upload/v1528005242/get_comic_request.png "Postman example")

The response it would be a JSON object with all the comics inside the DB

2. **CREATE COMIC**

Send POST request with token in the header to:

  ```
 POST https://python-comic-api.herokuapp.com/comics
  ```
  Inside the body, send a JSON object with the name of the Comic that the user wants to add to the DB (see image for example)
  ![alt text](http://res.cloudinary.com/jrleon90/image/upload/v1528005499/create_comic.png "Postman example")
  
  If everything works fine, the API will response with a succesfull messages (the user can use the GET all comics to validate that it works)
  
3. **LIKE COMIC**
  
 Send POST request with token in the header to:

  ```
 POST https://python-comic-api.herokuapp.com/comics/<comic_id>
  ```

  Replace <comic_id> with the Id of the comic that you want to give a Like.
  
  If everything works fine, the API will response with a succesfull messages (the user can use the GET all comics to validate that it works)  
  
  4. **CREATE NEW USER**
  
  Send POST request to:
  
   ```
 POST https://python-comic-api.herokuapp.com/user
  ```
  
  With the request, send username and password inside the body in JSON format (see image)
  
  ![alt text](http://res.cloudinary.com/jrleon90/image/upload/v1528007009/user_create.png "Postman Example")
