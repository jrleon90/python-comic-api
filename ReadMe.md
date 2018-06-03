# Python Comic API
## Table of Content
1. [Introduction](#introduction)
2. [Live example](#example)
3. [API Docs](#api_docs)



## Introduction <a name="introduction"></a>
This is an API developed with Python using Flask and JWT in order to have secure routes.

## Live Example <a name="example"></a>
There is a Live example for this API deployed in Heroku. In order to start you have to make a request to the following URI 
```
https://python-comic-api.herokuapp.com/
```
## API Docs <a name="api_docs"></a>
1. The API routes are protected with JWT, so in order to use the routes, you need to login, to do this send a GET request with Basic Auth (see image)
![alt text](http://res.cloudinary.com/jrleon90/image/upload/v1528004591/login_comic_api.png "Postman example")
  The request has to be made to the following URI
  ```
 GET https://python-comic-api.herokuapp.com/login
  ```
  Once the request has been made with a valid login information, it returns a token that needs to be save in order to made every request.
  
  2. **GET COMICS**

Send GET request to
  ```
 GET https://python-comic-api.herokuapp.com/comics
  ```
Since the routes are protected, the user needs to send the token in the header of the request with the key name "x-access-token" (see image)
![alt text](http://res.cloudinary.com/jrleon90/image/upload/v1528005242/get_comic_request.png "Postman example")

The response it would be a JSON object with all the comics inside the DB

3. **CREATE COMIC**

Send POST request with token in the header to:

  ```
 POST https://python-comic-api.herokuapp.com/comics
  ```
  Inside the body, send JSON object with name of the Comic that the user want to add to the DB (see image for example)
  ![alt text](http://res.cloudinary.com/jrleon90/image/upload/v1528005499/create_comic.png "Postman example")
  
  If everything works fine, the API will response with a succesfull messages (the user can use the GET all comics to validate that it works)
  
  4. **LIKE COMIC**
  
  Send POST request with token in the header to:

  ```
 POST https://python-comic-api.herokuapp.com/comics/<comic_id>
  ```

  Replace <comic_id> with the Id of the comic that you want to give a Like.
  
  If everything works fine, the API will response with a succesfull messages (the user can use the GET all comics to validate that it works)  
  
  5. **CREATE NEW USER**
  
  Send POST request to:
  
   ```
 POST https://python-comic-api.herokuapp.com/user
  ```
  
  With the request, send username and password inside the body in JSON format (see image)
  
  ![alt text](http://res.cloudinary.com/jrleon90/image/upload/v1528007009/user_create.png "Postman Example")
