from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('')
db = client['motor']
collection = db['motor']

@app.route('/display', methods=['GET'])
def display_collection():
    data = []
    for record in collection.find():
        data.append({
            "_id": str(record['_id']),
            "vehicle_id": record.get("vehicle_id", ""),
            "input": record.get("input", {}),
            "output": record.get("output", {})
        })

    return jsonify(data)

@app.route('/create_user', methods=['POST'])
def create_record():
    data = request.json

    if not data:
        return jsonify({"error": "Invalid request, data missing"}), 400

    vehicle_id = data.get("vehicle_id")
    input_data = data.get("input", {})
    output_data = data.get("output", {})

    new_record = {
        "vehicle_id": vehicle_id,
        "input": input_data,
        "output": output_data
    }

    collection.insert_one(new_record)

    return jsonify({"message": "Record created successfully"}), 201

@app.route('/update_user/<record_id>', methods=['POST'])
def update_record(record_id):
    data = request.json

    vehicle_id = data.get("vehicle_id")
    input_data = data.get("input", {})
    output_data = data.get("output", {})

    updated_record = {
        "vehicle_id": vehicle_id,
        "input": input_data,
        "output": output_data
    }

    result = collection.update_one({'_id': ObjectId(record_id)}, {'$set': updated_record})

    if result.modified_count == 1:
        return jsonify({"message": "Record updated successfully"})
    else:
        return jsonify({"error": "Record not found or not updated"}), 404

@app.route('/delete/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    result = collection.delete_one({'_id': ObjectId(record_id)})
    if result.deleted_count == 1:
        return jsonify({"message": "Record with ID {} deleted successfully".format(record_id)})
    else:
        return jsonify({"error": "Record with ID {} not found".format(record_id)}), 404

if __name__ == "__main__":
    app.run(debug=True)
