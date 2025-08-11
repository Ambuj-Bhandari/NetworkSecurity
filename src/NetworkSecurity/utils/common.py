from src.NetworkSecurity.exception.exception import NetworkSecurityException
from src.NetworkSecurity.logging.logger import logging
import yaml
from pymongo import MongoClient
import os,sys
# import dill
import numpy as np
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
    

def save_numpy_array_data(file_path:str,array:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file:
            np.save(file,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

def save_object(file_path:str, obj:object) ->None:
    try:
        logging.info("Entered the save object method of Utils ")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file:
            pickle.dump(obj,file)
        logging.info("Exiting the save object method of Utils ")
    except Exception as e:
        raise NetworkSecurityException(e,sys)