# app/database/mongo.py
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

client: MongoClient | None = None
db = None

def connect_to_mongo():
    global client, db

    MONGODB_URI = os.getenv("MONGODB_URI")
    if not MONGODB_URI:
        raise RuntimeError("MONGODB_URI is not set")

    client = MongoClient(MONGODB_URI, server_api=ServerApi("1"))
    client.admin.command("ping")

    db = client["CompanionAI"]
    print("✅ MongoDB connected")


def close_mongo_connection():
    global client
    if client:
        client.close()
        print("🔌 MongoDB disconnected")
