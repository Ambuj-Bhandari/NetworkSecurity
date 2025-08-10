from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()


def create_db_connection() -> MongoClient:
    conn = MongoClient(os.getenv('MONGO_DB_URI'))
    return conn
    