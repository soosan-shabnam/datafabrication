from datetime import datetime
import faker
import pymongo
from flask import Flask, jsonify, Response
import json

app = Flask(__name__)
fake = faker.Faker()


def db_connect():
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb+srv://suzie:suzie2002@cluster0.7r5huz7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    # Replace 'your_database' with the name of your MongoDB database
    db = client["fabrication"]
    return db

#pycharm sucks


def create_collection():
    # Create a collection named 'customer' if it doesn't exist
    db = db_connect()
    collection = db["customer"]
    return collection


def populate_collection_with_fakes():
    # Populate the collection with fake data
    collection = create_collection()

    for i in range(10, 101):
        customer = {
            "customer_id": i,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "address": fake.address(),
            "phone_number": fake.phone_number(),
            "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=70).isoformat()
            # MongoDB stores dates as ISODate
        }
        collection.insert_one(customer)


@app.route('/customers', methods=["GET"])
def get_customers():
    # Retrieve customers from MongoDB
    collection = create_collection()
    customers = collection.find()

    # Convert MongoDB documents to Python dictionaries
    customers_list = [customer for customer in customers]

    # Serialize Python dictionaries to JSON
    json_data = json.dumps(customers_list, default=str)  # Use default=str to serialize datetime objects

    return Response(json_data, content_type='application/json')


if __name__ == '__main__':
    populate_collection_with_fakes()
