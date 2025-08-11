from src.NetworkSecurity.exception.exception import NetworkSecurityException
from src.NetworkSecurity.logging.logger import logging
from src.NetworkSecurity.entity.config_entity import DataValidationConfig
from src.NetworkSecurity.entity.artifact_entity import DataValidationArtifacts,DataIngestionArtifacts
from src.NetworkSecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from src.NetworkSecurity.utils.common import read_yaml_file,write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import numpy as np
import os,sys


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifacts,
                 data_validation_config:DataValidationConfig):
        
        try:
            self.data_ingestion_artifacts = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def validate_number_columns(self,dataframe:pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self.schema_config['columns'])
            logging.info(f"Required number of columns = {number_of_columns}")
            logging.info(f"DataFrame has columns= {len(dataframe.columns)}")
            
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    
    def detect_data_drift(self,base_df,current_df,threshold=0.05) -> bool:
        try:
            status = True
            report={}
            
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                
                is_sample_dist = ks_2samp(d1,d2)
                
                if threshold<=is_sample_dist.pvalue:
                    is_found = False
                else:
                    is_found=True
                    status=False
                    
                report.update({column:{
                    "p_value":float(is_sample_dist.pvalue),
                    "drift_status":is_found
                }})
                
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_name = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_name,exist_ok=True)
            
            write_yaml_file(file_path=drift_report_file_path,content=report)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    
    def initiate_data_validation(self) -> DataValidationArtifacts:
        try:
            train_file_path = self.data_ingestion_artifacts.train_file_path
            test_file_path = self.data_ingestion_artifacts.test_file_path
            
            train_data = DataValidation.read_data(train_file_path)
            test_data = DataValidation.read_data(test_file_path)
            
            status = self.validate_number_columns(dataframe=train_data)
            if not status:
                error_message = "Train DataFrame does not contain all columns\n"
            status = self.validate_number_columns(dataframe=test_data)
            if not status:
                error_message = "Test DataFrame does not contain all columns\n"
            
            ##checking data Drift
            status = self.detect_data_drift(base_df=train_data,current_df=test_data)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            train_data.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
            test_data.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)
            
            
            data_validation_artifact = DataValidationArtifacts(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        