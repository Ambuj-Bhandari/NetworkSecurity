from src.NetworkSecurity.exception.exception import NetworkSecurityException
from src.NetworkSecurity.logging.logger import logging
from src.NetworkSecurity.entity.artifact_entity import DataValidationArtifacts,DataTransformationArtifacts
from src.NetworkSecurity.entity.config_entity import DataTransformationConfig
from src.NetworkSecurity.constants.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAMS
from src.NetworkSecurity.utils.common import save_numpy_array_data,save_object

import os,sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

class DataTransformation:
    def __init__(self,
                 data_validation_artifact:DataValidationArtifacts,
                 data_transformation_config:DataTransformationConfig
                 ):
    
        try:
            self.data_validation_artifact= data_validation_artifact
            self.data_transformation_config = data_transformation_config
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(file_path:str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def get_data_transformer_obj(cls)->Pipeline:
        """
        Initializes the KNNImputer object with parameters specified in
        training_pipeline.py file and returns a Pipeline object with KNNImputer object as First step
        """

        logging.info("Entered get_data_transformer_obj method")
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            preprocessor = Pipeline([(
                "imputer",imputer
            )])
            return preprocessor
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_transformation(self) -> DataTransformationArtifacts:
        logging.info("Entered initiate Data Transformation method")
        
        try:
            logging.info("Stating Data Transformation")
            train_data = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_data = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            ##Training Dataframe
            input_feature_train_df = train_data.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_data[TARGET_COLUMN]
            target_feature_train_df = train_data[TARGET_COLUMN].replace(-1,0)
            
            ##Testing Dataframe
            input_feature_test_df = test_data.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = test_data[TARGET_COLUMN]
            target_feature_test_df = test_data[TARGET_COLUMN].replace(-1,0)
            
            preprocessor = self.get_data_transformer_obj()
            preprocessor_obj = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_obj.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_obj.transform(input_feature_test_df)
            
            train_arr = np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature,np.array(target_feature_test_df)]
            
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_obj)
            
            #Preparing Artifacts
            data_transformation_artifact = DataTransformationArtifacts(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
