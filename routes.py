from myapp import app
from flask import request,make_response,jsonify
from functools import wraps
import jwt
import os
import datetime
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash 


#Function to validate Token
def token_verification(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        #Search for token inside the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        #If there is no token, send response with message
        if not token:
            return make_response('Token is missing', 401,{'WWW-authenticate' : 'Basic realm="Login required!"'})

        #Decode token and find get information of the current user
        try:
            token_decoded = jwt.decode(token,app.config['SECRET_KEY'])

            current_user = search_user(token_decoded['username'])

        #if token expired, send messages and abort the process
        except jwt.ExpiredSignature:
            return make_response('Token expired', 401,{'WWW-authenticate' : 'Basic realm="Login required!"'})
      
        #If there is an error in the password, send message and abort process
        except jwt.DecodeError:
            return make_response('Could not decode token', 401,{'WWW-authenticate' : 'Basic realm="Login required!"'})
      
        return f(current_user,*args,**kwargs)
   
    return decorated


#Index Route
@app.route('/')
def index():
    return jsonify({'message':'Welcome to the comic APIs'})


#GET All comics
@app.route('/comics',methods=['GET'])
@token_verification
def get_all_comics(current_user):
    
    #Connection instance to MySQL Database
    cnx = mysql.connector.connect(user=app.config['MYSQL_DATABASE_USER'],password=app.config['MYSQL_DATABASE_PASSWORD'],host=app.config['MYSQL_DATABASE_HOST'],database=app.config['MYSQL_DATABASE_DB'])

    cursor = cnx.cursor()
   
    query = ('''SELECT * FROM comic_book''')
    cursor.execute(query)

    row_headers=[x[0] for x in cursor.description]


    data = cursor.fetchall()
    json_data = []

    #Loop to add column names to JSON file and data
    for item in data:
        json_data.append(dict(zip(row_headers,item)))

    cursor.close()
    cnx.close()

    return jsonify({'comics' : json_data})

#Create a Comic
@app.route('/comics',methods=['POST'])
@token_verification
def create_comic(current_user):

    #Connection instance to MySQL Database
    cnx = mysql.connector.connect(user=app.config['MYSQL_DATABASE_USER'],password=app.config['MYSQL_DATABASE_PASSWORD'],host=app.config['MYSQL_DATABASE_HOST'],database=app.config['MYSQL_DATABASE_DB'])

    cursor = cnx.cursor()
    add_comic = ("INSERT INTO comic_book "
            "(name, likes) "
            "VALUES(%s, %s)")

    #Get Data inside body of request in JSON format
    data = request.get_json()

    #Comic data (comic name, number of likes 0 by default)
    comic_data = (str(data['name']),0)
    cursor.execute(add_comic, comic_data)

    cnx.commit()

    cursor.close()
    cnx.close()

    return jsonify({'message':'Comic added!'})

#Like a comic
@app.route('/comics/<comic_id>', methods=['POST'])
@token_verification
def like_comic(current_user, comic_id):

    #Connection instance to MySQL Database
    cnx = mysql.connector.connect(user=app.config['MYSQL_DATABASE_USER'],password=app.config['MYSQL_DATABASE_PASSWORD'],host=app.config['MYSQL_DATABASE_HOST'],database=app.config['MYSQL_DATABASE_DB'])

    cursor = cnx.cursor() 
    cursorB = cnx.cursor()

    #Query to find the comic
    query = ("SELECT likes FROM comic_book WHERE _id=%s")

    #Query to update the comic
    update_query = ("UPDATE comic_book SET likes = %s WHERE _id =%s")

    cursor.execute(query,(comic_id,))

    data = cursor.fetchall()

    #If there is no comic with the Id specified, abort process and send message
    if cursor.rowcount == 0:
        return make_response('Comic not found', 404)
 
    #If comic is found, Update row
    for likes in data:
        cursorB.execute(update_query,(likes[0]+1,comic_id))

    cnx.commit()
    cursor.close()
    cursorB.close()
    cnx.close()

    return jsonify({'message': 'Like update'})


#Create a new User
@app.route('/user',methods=['POST'])
def create_user():

    #Connection instance to MySQL Database
    cnx = mysql.connector.connect(user=app.config['MYSQL_DATABASE_USER'],password=app.config['MYSQL_DATABASE_PASSWORD'],host=app.config['MYSQL_DATABASE_HOST'],database=app.config['MYSQL_DATABASE_DB'])

    cursor = cnx.cursor()
    add_user = ("INSERT INTO user "
            "(username, password) "
            "VALUES(%s, %s)")

    #Get user data inside request body in JSON format
    data = request.get_json()

    #Encrypt user password
    hash_password = generate_password_hash(str(data['password']),method='sha256')
    user_data = (str(data['username']),hash_password)
    cursor.execute(add_user, user_data)

    cnx.commit()
    cursor.close()
    cnx.close()

    return jsonify({'message':'New User created!'})


#Login user to generate Token
@app.route('/login')
def login():
    auth = request.authorization

    #If there is no username or password, abort process and send message
    if not auth or not auth.username or not auth.password:
        return make_response('No username or password', 401,{'WWW-authenticate' : 'Basic realm="Login required!"'})
 
    #Look for user
    data = search_user(auth.username)

    #If there is no user, abort process and send message
    if not data:
        return make_response('User not found', 401,{'WWW-authenticate' : 'Basic realm="Login required!"'})
    
    #Validate user password
    if check_password_hash(data[1],auth.password):
        #Generate token
        token = jwt.encode({'_id':data[2],'username':data[0],'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30  )},app.config['SECRET_KEY'])
        return jsonify({'token':token.decode('UTF-8')})

    
    return make_response('Could not verify', 401,{'WWW-authenticate' : 'Basic realm="Login required!"'})

#Function to search a user by his/her username
def search_user(username):

    #Connection instance to MySQL Database
    cnx = mysql.connector.connect(user=app.config['MYSQL_DATABASE_USER'],password=app.config['MYSQL_DATABASE_PASSWORD'],host=app.config['MYSQL_DATABASE_HOST'],database=app.config['MYSQL_DATABASE_DB'])

    cursor = cnx.cursor()
    query = ("SELECT username,password,_id FROM user WHERE username='%s'"%(str(username)))
   
    cursor.execute(query) 

    data = cursor.fetchone()

    cursor.close()
    cnx.close()

    return data


if __name__ == '__main__':
    app.run(debug=True)