from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from pymongo import response

app = Flask(__name__)
app.config["MONGO_URI"]='mongodb://localhost/test'
mongo = PyMongo(app)

#ruta para agregar persona
@app.route('/users', methods=['POST'])
def create_user():

    _id = request.json['_id']
    nombre = request.json['nombre']
    apellido = request.json['apellido']

    if _id and nombre and apellido:
        mongo.db.users.insert(
            {'_id': _id, 'nombre': nombre, 'apellido': apellido}
        )
        response = {
            '_id': str(_id),
            'nombre': nombre,
            'apellido': apellido,          
        }
        return response
    else:
        return not_found()

    return {'message': 'received'}

#ruta para agregar pais
@app.route('/country', methods=['POST'])
def create_country():

    _id = request.json['_id']
    pais = request.json['pais']
    
    if _id and pais:
        mongo.db.paises.insert(
            {'_id': _id, 'pais': pais}
        )
        response = {
            '_id': str(_id),
            'pais': pais,           
        }
        return response
    else:
        return not_found()

    return {'message': 'received'}

#ruta para crear el estado y la ciudad
@app.route('/state', methods=['POST'])
def create_state():

    _id = request.json['_id']
    estado = request.json['estado']
    ciudad = request.json['ciudad']

    if _id and estado and ciudad:
        mongo.db.estados.insert(
            {'_id': _id, 'estado': estado, 'ciudad': ciudad}
        )
        response = {
            '_id': str(_id),
            'estado': estado,    
            'ciudad': ciudad,       
        }
        return response
    else:
        return not_found()

    return {'message': 'received'}

#obtener todos los paises
@app.route('/country', methods=['GET'])
def get_allcountries():

    paises = mongo.db.paises.find()
    response = json_util.dumps(paises)
    return Response(response, mimetype='application/json')

#obtener pais por id
@app.route('/country/<id>', methods=['GET'])
def get_countries(id):

    paises = mongo.db.paises.find_one({'_id': id})
    response = json_util.dumps(paises)
    return Response(response, mimetype='application/json')

#obtener todos los estados y ciudades
@app.route('/state', methods=['GET'])
def get_allstates():

    estados = mongo.db.estados.find()
    response = json_util.dumps(estados)
    return Response(response, mimetype='application/json')

#obtener ciudad y estado por id
@app.route('/state/<id>', methods=['GET'])
def get_states(id):

    estados = mongo.db.estados.find_one({'_id': id})
    response = json_util.dumps(estados)
    return Response(response, mimetype='application/json')

#obtener usuario por id
@app.route('/users/<id>', methods=['GET'])
def get_user(id):

    user = mongo.db.users.find_one({'_id': id})
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': id})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource Not found:' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True)