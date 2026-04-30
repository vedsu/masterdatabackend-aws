from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
import boto3
import json
import os
# from dotenv import load_dotenv

app = Flask(__name__)

# Access MongoDB Atlas Cluster
# load_dotenv()

secret_name = "aws-model"
region_name = 'us-east-1'


def get_secret(secret_name, region_name):
    
    try:

        session = boto3.session.Session()
        client = session.client(
            service_name = "secretsmanager",
            region_name = region_name
        )

        response = client.get_secret_value(SecretId = secret_name)
        secret_string = response["SecretString"]
        return json.loads(secret_string)
    
    except Exception as e:
        print(f"Error retrieving secret : {e}")
        return {}

secret_data = get_secret(secret_name, region_name)

app.config["MONGO_URI"] = secret_data["MONGODB_BW"]

mongo = PyMongo(app)

cors = CORS(app)

s3_resource = boto3.resource(
    service_name = "s3",
    region_name = 'us-east-1',
    aws_access_key_id = access_id,
    aws_secret_access_key = access_key

)
s3_client = boto3.client(
    service_name = "s3",
    region_name = 'us-east-1',
    aws_access_key_id = access_id,
    aws_secret_access_key = access_key)

from app import routes
