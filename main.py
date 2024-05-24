from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)


client = MongoClient('mongodb://localhost:27017/')
db = client['movies']
collection = db['hollywood']


# Create a Document in DB for each movie
@app.route('/addMovie', methods=['POST'])
def addMovie():
    data = request.json
    result = collection.insert_one(data)

    if result.acknowledged == True:
        id = str(result.inserted_id)
        return jsonify({
            'success': True,
            'message': 'Movie added successfully...',
            'data': id
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': 'Failed to add Movie to DB...',
        }), 400


# Read all Documents in collection 'hollywood'
@app.route('/readAll', methods=['GET'])
def readAll():
    data = list(collection.find())
    for document in data:
        document['_id'] = str(document['_id'])

    return jsonify({
            'success': True,
            'message': 'Read operation successful...',
            'data': data
        }), 200

# Update a Document in collection 'hollywood'
@app.route('/update/<string:id>', methods=['PUT'])
def update(id):
    object_id = ObjectId(id)
    data = request.json
    result = collection.update_one({'_id': object_id}, {'$set': data})
    if result.matched_count > 0:
        return jsonify({
            'success': True,
            'message': 'Data updated successfully...',
            'data': id
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': 'Document not found...',
        }), 404

# Delete a Document from collection 'hollywood'
@app.route('/delete/<string:id>', methods=['DELETE'])
def delete(id):
    object_id = ObjectId(id)
    result = collection.delete_one({'_id': object_id})
    if result.deleted_count > 0:
        return jsonify({
            'success': True,
            'message': 'Data deleted successfully...',
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': 'Document not found...',
        }), 404

if __name__ =='__main__':
    app.run(debug=True)