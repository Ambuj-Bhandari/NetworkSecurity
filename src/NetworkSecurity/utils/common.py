from src.NetworkSecurity.exception.exception import NetworkSecurityException
from src.NetworkSecurity.logging.logger import logging
import yaml
from pymongo import MongoClient
import os,sys
# import dill
import pickle
from dotenv import load_dotenv
load_dotenv()


def create_db_connection() -> MongoClient:
    conn = MongoClient(os.getenv('MONGO_DB_URI'))
    return conn
    
def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path,"rb") as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def write_yaml_file(file_path:str , content:object, replace:bool = False) ->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)