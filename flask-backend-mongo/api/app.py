from flask import Flask, request, jsonify  # Importa las clases Flask, request y jsonify del módulo flask
from bson.json_util import dumps  # Importa la función dumps del módulo bson.json_util
from bson.objectid import ObjectId  # Importa la clase ObjectId del módulo bson
import db  # Importa el módulo db (probablemente un módulo personalizado)
from flask_cors import CORS  # Importa la clase CORS del módulo flask_cors
import pymongo  # Importa el módulo pymongo
import json  # Importa el módulo json

app = Flask(__name__)  # Crea una instancia de la clase Flask con el nombre del módulo actual
CORS(app)  # Aplica el middleware CORS a la aplicación Flask

with open('productos.json') as file:  # Abre el archivo 'productos.json' en modo lectura y lo asigna a la variable 'file'
    productos_data = json.load(file)  # Carga el contenido del archivo JSON en la variable 'productos_data'

with open('clientes.json') as file:  # Abre el archivo 'clientes.json' en modo lectura y lo asigna a la variable 'file'
    clientes_data = json.load(file)  # Carga el contenido del archivo JSON en la variable 'clientes_data'

# Agrega los datos precargados en los archivos JSON a la base de datos
def add_productos():
    con = db.get_connection()  # Obtiene una conexión a la base de datos
    dbstore = con.dbstore  # Asigna la base de datos 'dbstore' a la variable 'dbstore'
    try:
        productos = dbstore.productos  # Obtiene la colección 'productos' de la base de datos
        productos.insert_many(productos_data)  # Inserta los datos de 'productos_data' en la colección 'productos'
        print("Productos agregados exitosamente")  # Imprime un mensaje indicando que los productos se agregaron exitosamente
    finally:
        con.close()  # Cierra la conexión a la base de datos
        print("Connection closed")  # Imprime un mensaje indicando que la conexión se cerró

# Agrega los datos precargados en los archivos JSON a la base de datos
def add_clientes():
    con = db.get_connection()  # Obtiene una conexión a la base de datos
    dbstore = con.dbstore  # Asigna la base de datos 'dbstore' a la variable 'dbstore'
    try:
        clientes = dbstore.clientes  # Obtiene la colección 'clientes' de la base de datos
        clientes.insert_many(clientes_data)  # Inserta los datos de 'clientes_data' en la colección 'clientes'
        print("Clientes agregados exitosamente")  # Imprime un mensaje indicando que los clientes se agregaron exitosamente
    finally:
        con.close()  # Cierra la conexión a la base de datos
        print("Connection closed")  # Imprime un mensaje indicando que la conexión se cerró

# Define el endpoint para obtener todos los productos
@app.route("/productos", methods=['GET'])
def get_productos():
    con = db.get_connection()  # Obtiene una conexión a la base de datos
    dbstore = con.dbstore  # Asigna la base de datos 'dbstore' a la variable 'dbstore'
    try:
        productos = dbstore.productos  # Obtiene la colección 'productos' de la base de datos
        response = app.response_class(
            response=dumps(productos.find()),  # Obtiene todos los documentos de la colección 'productos' y los convierte a formato JSON
            status=200,  # Establece el código de estado de la respuesta a 200 (éxito)
            mimetype='application/json'  # Establece el tipo MIME de la respuesta a 'application/json'
        )
        return response  # Devuelve la respuesta
    finally:
        con.close()  # Cierra la conexión a la base de datos
        print("Connection closed")  # Imprime un mensaje indicando que la conexión se cerró

# Define el endpoint para obtener un producto por su ID
@app.route("/productos/<producto_id>", methods=['GET'])
def get_producto(producto_id):
    con = db.get_connection()  # Obtiene una conexión a la base de datos
    dbstore = con.dbstore  # Asigna la base de datos 'dbstore' a la variable 'dbstore'
    try:
        productos = dbstore.productos  # Obtiene la colección 'productos' de la base de datos
        response = app.response_class(
            response=dumps(productos.find_one({'_id': ObjectId(producto_id)})),  # Obtiene un documento de la colección 'productos' por su ID y lo convierte a formato JSON
            status=200,  # Establece el código de estado de la respuesta a 200 (éxito)
            mimetype='application/json'  # Establece el tipo MIME de la respuesta a 'application/json'
        )
        return response  # Devuelve la respuesta
    finally:
        con.close()  # Cierra la conexión a la base de datos
        print("Connection closed")  # Imprime un mensaje indicando que la conexión se cerró

# Define el endpoint para crear un producto
@app.route("/productos", methods=['POST'])
def create_producto():
    data = request.get_json()  # Obtiene los datos JSON enviados en la solicitud
    con = db.get_connection()  # Obtiene una conexión a la base de datos
    dbstore = con.dbstore  # Asigna la base de datos 'dbstore' a la variable 'dbstore'
    try:
        productos = dbstore.productos  # Obtiene la colección 'productos' de la base de datos
        result = productos.insert_one(data)  # Inserta los datos en la colección 'productos'
        return jsonify({"message": "Amo chat gpt", "_id": str(result.inserted_id)}), 201  # Devuelve una respuesta JSON con un mensaje de éxito y el ID del producto creado
    finally:
        con.close()  # Cierra la conexión a la base de datos
        print("Connection closed")  # Imprime un mensaje indicando que la conexión se cerró

# Define el endpoint para actualizar un producto por su ID
@app.route("/productos/<producto_id>", methods=['PUT'])
def update_producto(producto_id):
    data = request.get_json()  # Obtiene los datos JSON enviados en la solicitud
    con = db.get_connection()  # Obtiene una conexión a la base de datos
    dbstore = con.dbstore  # Asigna la base de datos 'dbstore' a la variable 'dbstore'
    try:
        productos = dbstore.productos  # Obtiene la colección 'productos' de la base de datos
        result = productos.update_one({'_id': ObjectId(producto_id)}, {'$set': data})  # Actualiza el documento de la colección 'productos' con el ID dado usando los nuevos datos
        if result.modified_count > 0:  # Si se modificó al menos un documento
            return jsonify({"message": "Producto actualizado exitosamente"}), 200  # Devuelve una respuesta JSON con un mensaje de éxito y código de estado 200
        else:
            return jsonify({"message": "Producto no encontrado"}), 404  # Devuelve una respuesta JSON con un mensaje de error y código de estado 404
    finally:
        con.close()  # Cierra la conexión a la base de datos
        print("Connection closed")  # Imprime un mensaje indicando que la conexión se cerró

# Define el endpoint para eliminar un producto por su ID
@app.route("/productos/<producto_id>", methods=['DELETE'])
def delete_producto(producto_id):
    con = db.get_connection()  # Obtiene una conexión a la base de datos
    dbstore = con.dbstore  # Asigna la base de datos 'dbstore' a la variable 'dbstore'
    try:
        productos = dbstore.productos  # Obtiene la colección 'productos' de la base de datos
        result = productos.delete_one({'_id': ObjectId(producto_id)})  # Elimina el documento de la colección 'productos' con el ID dado
        if result.deleted_count > 0:  # Si se eliminó al menos un documento
            return jsonify({"message": "Producto eliminado exitosamente"}), 200  # Devuelve una respuesta JSON con un mensaje de éxito y código de estado 200
        else:
            return jsonify({"message": "Producto no encontrado"}), 404  # Devuelve una respuesta JSON con un mensaje de error y código de estado 404
    finally:
        con.close()  # Cierra la conexión a la base de datos
        print("Connection closed")  # Imprime un mensaje indicando que la conexión se cerró

# Define el endpoint para obtener todos los clientes
@app.route("/clientes", methods=['GET'])
def get_clientes():
    con = db.get_connection()  # Obtiene una conexión a la base de datos
    dbstore = con.dbstore  # Asigna la base de datos 'dbstore' a la variable 'dbstore'
    try:
        clientes = dbstore.clientes  # Obtiene la colección 'clientes' de la base de datos
        response = app.response_class(
            response=dumps(clientes.find()),  # Obtiene todos los documentos de la colección 'clientes' y los convierte a formato JSON
            status=200,  # Establece el código de estado de la respuesta a 200 (éxito)
            mimetype='application/json'  # Establece el tipo MIME de la respuesta a 'application/json'
        )
        return response  # Devuelve la respuesta
    finally:
        con.close()  # Cierra la conexión a la base de datos
        print("Connection closed")  # Imprime un mensaje indicando que la conexión se cerró

# Define el endpoint para obtener un cliente por su ID
@app.route("/clientes/<cliente_id>", methods=['GET'])
def get_cliente(cliente_id):
    con = db.get_connection()  # Obtiene una conexión a la base de datos
    dbstore = con.dbstore  # Asigna la base de datos 'dbstore' a la variable 'dbstore'
    try:
        clientes = dbstore.clientes  # Obtiene la colección 'clientes' de la base de datos
        response = app.response_class(
            response=dumps(clientes.find_one({'_id': ObjectId(cliente_id)})),  # Obtiene un documento de la colección 'clientes' por su ID y lo convierte a formato JSON
            status=200,  # Establece el código de estado de la respuesta a 200 (éxito)
            mimetype='application/json'  # Establece el tipo MIME de la respuesta a 'application/json'
        )
        return response  # Devuelve la respuesta
    finally:
        con.close()  # Cierra la conexión a la base de datos
        print("Connection closed")  # Imprime un mensaje indicando que la conexión se cerró

# Define el endpoint para crear un cliente
@app.route("/clientes", methods=['POST'])
def create_cliente():
    data = request.get_json()  # Obtiene los datos JSON enviados en la solicitud
    con = db.get_connection()  # Obtiene una conexión a la base de datos
    dbstore = con.dbstore  # Asigna la base de datos 'dbstore' a la variable 'dbstore'
    try:
        clientes = dbstore.clientes  # Obtiene la colección 'clientes' de la base de datos
        result = clientes.insert_one(data)  # Inserta los datos en la colección 'clientes'
        return jsonify({"message": "Cliente creado exitosamente", "_id": str(result.inserted_id)}), 201  # Devuelve una respuesta JSON con un mensaje de éxito y el ID del cliente creado
    finally:
        con.close()  # Cierra la conexión a la base de datos
        print("Connection closed")  # Imprime un mensaje indicando que la conexión se cerró

# Define el endpoint para actualizar un cliente por su ID
@app.route("/clientes/<cliente_id>", methods=['PUT'])
def update_cliente(cliente_id):
    data = request.get_json()  # Obtiene los datos JSON enviados en la solicitud
    con = db.get_connection()  # Obtiene una conexión a la base de datos
    dbstore = con.dbstore  # Asigna la base de datos 'dbstore' a la variable 'dbstore'
    try:
        clientes = dbstore.clientes  # Obtiene la colección 'clientes' de la base de datos
        result = clientes.update_one({'_id': ObjectId(cliente_id)}, {'$set': data})  # Actualiza el documento de la colección 'clientes' con el ID dado usando los nuevos datos
        if result.modified_count > 0:  # Si se modificó al menos un documento
            return jsonify({"message": "Cliente actualizado exitosamente"}), 200  # Devuelve una respuesta JSON con un mensaje de éxito y código de estado 200
        else:
            return jsonify({"message": "Cliente no encontrado"}), 404  # Devuelve una respuesta JSON con un mensaje de error y código de estado 404
    finally:
        con.close()  # Cierra la conexión a la base de datos
        print("Connection closed")  # Imprime un mensaje indicando que la conexión se cerró

# Define el endpoint para eliminar un cliente por su ID
@app.route("/clientes/<cliente_id>", methods=['DELETE'])
def delete_cliente(cliente_id):
    con = db.get_connection()  # Obtiene una conexión a la base de datos
    dbstore = con.dbstore  # Asigna la base de datos 'dbstore' a la variable 'dbstore'
    try:
        clientes = dbstore.clientes  # Obtiene la colección 'clientes' de la base de datos
        result = clientes.delete_one({'_id': ObjectId(cliente_id)})  # Elimina el documento de la colección 'clientes' con el ID dado
        if result.deleted_count > 0:  # Si se eliminó al menos un documento
            return jsonify({"message": "Cliente eliminado exitosamente"}), 200  # Devuelve una respuesta JSON con un mensaje de éxito y código de estado 200
        else:
            return jsonify({"message": "Cliente no encontrado"}), 404  # Devuelve una respuesta JSON con un mensaje de error y código de estado 404
    finally:
        con.close()  # Cierra la conexión a la base de datos
        print("Connection closed")  # Imprime un mensaje indicando que la conexión se cerró

if __name__ == "__main__":
    add_clientes()  # Agrega los datos preexistentes de los clientes a la base de datos
    add_productos()  # Agrega los datos preexistentes de los productos a la base de datos
    app.run()  # Inicia el servidor Flask para escuchar las solicitudes entrantes
