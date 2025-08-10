from src.NetworkSecurity.exception.exception import NetworkSecurityException
from src.NetworkSecurity.logging.logger import logging
from src.NetworkSecurity.entity.config_entity import DataIngestionConfig
from src.NetworkSecurity.utils.common import create_db_connection
from src.NetworkSecurity.entity.artifact_entity import DataIngestionArtifacts
import os
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def export_collection_as_Dataframe(self):
        try:
            db_name = self.data_ingestion.database_name
            collection_name = self.data_ingestion.collection_name
            
            mongo_client = create_db_connection()
            collection = mongo_client[db_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df.drop(columns=["_id"],inplace=True,axis=1)
            
            df.replace({"na":np.nan},inplace=True)
            return df
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion.feature_store_file_path
            
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            dataframe.to_csv(self.data_ingestion.feature_store_file_path,index=False,header=True)
            return dataframe
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    
    def split_data_into_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set, test_set = train_test_split(dataframe,test_size=self.data_ingestion.spli_ratio)

            logging.info("Performed train Test Split on dataframe")
            logging.info("Exiting split_data_into_train_test method of DataIngestion Class")
            
            dir_path = os.path.dirname(self.data_ingestion.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            logging.info("Exporting data to Training and testing file paths")
            
            train_set.to_csv(self.data_ingestion.training_file_path,index=False,header = True)
            
            test_set.to_csv(self.data_ingestion.testing_file_path,index=False,header = True)
            
            logging.info("Exported train and test files")
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def initiate_data_ingestion(self):
        try:
            df = self.export_collection_as_Dataframe()
            df = self.export_data_into_feature_store(dataframe=df)
            self.split_data_into_train_test(dataframe=df)
            
            data_ingestion_artifacts = DataIngestionArtifacts(self.data_ingestion.training_file_path,
                                                              self.data_ingestion.testing_file_path)
            
            return data_ingestion_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)