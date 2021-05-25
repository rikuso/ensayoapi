from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo, ObjectId
from bson import json_util
from bson.objectid import ObjectId
import json

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = 'myawesomesecretkey'

app.config['MONGO_URI'] = 'mongodb://localhost:27017/ensayorest'

mongo = PyMongo(app)


@app.route('/post', methods=['POST'])
def create_user():
    # Receiving Data
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    menu = request.json['menu']
    menu_name = request.json['menu_name']
    menu_descripcion = request.json['menu_descripcion']
    if username and email and password:
        hashed_password = generate_password_hash(password)
        #preguitar si quiere añadir nuevos valores a menu s
        agregados =["categoria daniel"]
        runnig = True
        while runnig:
            menu_name= str(input('campo de nombre :'))
            menu_descripcion= str(input('campo de descripcion :'))
            valu={'menu_name':menu_name,
                    'menu_descripcion':menu_descripcion}
            agregados.append(valu)

            agregar_mas=  input("queires agregar mas s/n: ")
            if agregar_mas == 'n':
                runnig= False
                    
        id = mongo.db.users.insert(
        {'username': username, 'email': email, 'password': hashed_password, 'menu':agregados})


        response = jsonify({
            '_id': str(id),
            'username': username
        })
        response.status_code = 201
        return response
    else:
        return not_found()
    

@app.route('/get', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")


@app.route('/get/<id>', methods=['GET'])
def get_user(id):
    print(id)
    user = mongo.db.users.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(user)

    documentos= mongo.db.users.find_one({
            'menu_name': 'arroz'
        })
    print(f'el documento a buscar : {documentos}')

    return Response(response, mimetype="application/json")


@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):

    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response



@app.route('/put/<_id>', methods=['PUT'])
def update_user(_id):
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    if username and email and password and _id:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'username': username, 'email': email, 'password': hashed_password}})
        response = jsonify({'message': 'User' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)