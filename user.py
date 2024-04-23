from flask import Flask, render_template, jsonify, request
import json
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('mongodb+srv://guselvaraanni24:Selvaraanni%4024@cluster0.e1quzum.mongodb.net/')
db = client['user']
collection = db['user']


@app.route('/display', methods=['GET'])
def display_collection():
    collection_name = 'user'
    user_collection = db.get_collection(collection_name)
    if user_collection is None:
        return jsonify({"error": f"Collection {collection_name} not found"}), 404

    data = []
    for record in user_collection.find():
        data.append({
            "_id": str(record['_id']),
            "email": record.get("email", ""),
            "password": record.get("password", "")
        })

    return jsonify(data)

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json

    if not data:
        return jsonify({"error": "Invalid request, data missing"}), 400

    email = data.get("email")
    password = data.get("password")

    existing_user = collection.find_one({"email": email})
    if existing_user:
        return jsonify({"error": "Username already exists"}), 409

    new_user = {
        "email": email,
        "password": password
    }

    collection.insert_one(new_user)

    return jsonify({"message": "User created successfully"}), 201

@app.route('/update_user/<user_id>', methods=['GET'])
def show_update_user_form(user_id):
    user = collection.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({"error": f"User with ID {user_id} not found"}), 404

    return jsonify({
        "email": user["email"],
        "password": user["password"]
    })

@app.route('/update_user', methods=['POST' ])
def update_password():
    data = request.json
    email = data.get("email")
    new_password = data.get("password")

    if not email or not new_password:
        return jsonify({"error": "Invalid request, username or new_password missing"}), 400

    user = collection.find_one({"email": email})

    if not user:
        return jsonify({"error": f"User with username {email} not found"}), 404

    collection.update_one(
        {'_id': user['_id']},
        {'$set': {'password': new_password}}
    )

    return jsonify({"message": "Password updated successfully"}), 200

@app.route('/delete/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user_id = ObjectId(user_id)
        result = collection.delete_one({'_id': user_id})
        if result.deleted_count == 1:
            return jsonify({"message": f"User with ID {user_id} deleted successfully"})
        else:
            return jsonify({"error": f"User with ID {user_id} not found"}), 404
    except ValueError:
        return jsonify({"error": f"Invalid user ID format: {user_id}"}), 400

if __name__ == "__main__":
    app.run(debug=True)