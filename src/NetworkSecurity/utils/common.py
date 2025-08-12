from src.NetworkSecurity.exception.exception import NetworkSecurityException
from src.NetworkSecurity.logging.logger import logging
import yaml
from pymongo import MongoClient
import os,sys
# import dill
import numpy as np
import pickle
from dotenv import load_dotenv
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
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
    

def load_object(file_path:str) ->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exists")
        with open(file_path,"rb") as file:
            return pickle.load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_numpy_array_data(file_path:str) -> np.array:
    try:
        with open(file_path,"rb") as file:
            return np.load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def evaluate_model(X_train, Y_train, X_test, Y_test, models, params):
    try:
        report={}
        for name , model in models.items():
            para = params[name]
            
            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,Y_train)
            
            model.set_params(**gs.best_params_)
            model.fit(X_train,Y_train)
            
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            
            train_model_score = r2_score(Y_train,y_train_pred)
            test_model_score = r2_score(Y_test,y_test_pred)
            
            report[name] = test_model_score
        
        return report
             
    except Exception as e:
        raise NetworkSecurityException(e,sys)