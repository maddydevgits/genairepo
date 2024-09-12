from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client['legal_aid']
complaints_collection = db['complaints']

def save_complaint(complaint_data):
    result = complaints_collection.insert_one(complaint_data)
    return result.inserted_id

def get_complaint_status(complaint_id):
    complaint = complaints_collection.find_one({"_id": ObjectId(complaint_id)})
    return complaint.get('status', 'Unknown') if complaint else None
