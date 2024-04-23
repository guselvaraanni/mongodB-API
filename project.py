from flask import Flask, render_template, jsonify, request
from bson.objectid import ObjectId
from pymongo import MongoClient
app = Flask(__name__)

client = MongoClient('mongodb+srv://guselvaraanni24:Selvaraanni%4024@cluster0.e1quzum.mongodb.net/')
db = client['project']
collection = db['project']

@app.route('/display', methods=['GET'])
def display_collection():
    user_collection = db['project']
    if user_collection is None:
        return jsonify({"error": "Collection project not found"}), 404

    data = []
    for record in user_collection.find():
        data.append({
            "_id": str(record['_id']),
            "user_id": record.get("user_id", ""),
            "vehicle_no": record.get("vehicle_no", "")
        })

    return jsonify(data)

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json

    if not data:
        return jsonify({"error": "Invalid request, data missing"}), 400

    user_id = data.get("user_id")
    vehicle_no = data.get("vehicle_no")

    existing_user = collection.find_one({"user_id": user_id})
    if existing_user:
        return jsonify({"error": "Username already exists"}), 409

    new_user = {
        "user_id": user_id,
        "vehicle_no": vehicle_no
    }

    collection.insert_one(new_user)

    return jsonify({"message": "User created successfully"}), 201

@app.route('/update_user/<user_id>', methods=['GET'])
def show_update_user_form(_id):
    project = collection.find_one({'_id': ObjectId(_id)})
    if not project:
        return jsonify({"error": f"User with ID {_id} not found"}), 404

    return jsonify({
        "id": str(project["_id"]),
        "user_id": project["user_id"],
        "vehicle_no": project["vehicle_no"]
    })

@app.route('/update_user', methods=['POST' ])
def update_vehicle_no():
    data = request.json
    user_id = data.get("user_id")
    vehicle_no = data.get("vehicle_no")

    if not user_id or not vehicle_no:
        return jsonify({"error": "Invalid request, username or new_password missing"}), 400

    user = collection.find_one({"user_id": user_id})

    if not user:
        return jsonify({"error": f"User with user_id {user_id} not found"}), 404

    collection.update_one(
        {'_id': user['_id']},
        {'$set': {'vehicle_no': vehicle_no}}
    )

    return jsonify({"message": "Vehicle number updated successfully"}), 200

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
