import os
import sys
import json
from dotenv import load_dotenv
import certifi
import pandas as pd
from pymongo import MongoClient
import numpy as np
from src.NetworkSecurity.logging.logger import logging
from src.NetworkSecurity.exception.exception import NetworkSecurityException

load_dotenv()
ca = certifi.where()

class NetworkDataExtract():
    def __init__(self,database,collections):
        try:
            self.database = database
            self.collection = collections
            self.mongo_uri = os.getenv("MONGO_DB_URI")
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def csv_to_json_convertor(self,file_path):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True,inplace=True)
            records = list(json.loads(df.T.to_json()).values())
            return records
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def insert_data_to_mongodb(self,records,):
        try:
            mongo_client = MongoClient(self.mongo_uri)
            db = mongo_client[self.database]
            collection = db[self.collection]
            
            collection.insert_many(records)
            return len(records)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

if __name__ == "__main__":
    file_path = r"D:\Projects\ML\End-To-End ML Projects\NetworkSecurity\Network Data\Dataset Phising Website.csv"
    Database = "Ambuj"
    Collection = "NetworkData"
    
    networkobj = NetworkDataExtract(database=Database,collections=Collection)
    records = networkobj.csv_to_json_convertor(file_path=file_path)
    print(records)
    no_of_records = networkobj.insert_data_to_mongodb(records=records)
    print(no_of_records)
            



