from src.NetworkSecurity.conponents.data_ingestion import DataIngestion
from src.NetworkSecurity.conponents.data_validation import DataValidation
from src.NetworkSecurity.conponents.data_transformation import DataTransformation
from src.NetworkSecurity.exception.exception import NetworkSecurityException
from src.NetworkSecurity.logging.logger import logging
from src.NetworkSecurity.entity.config_entity import (DataIngestionConfig,
                                                      TrainingPipelineConfig,
                                                      DataValidationConfig,
                                                      DataTransformationConfig)
import sys


def main():
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        
        logging.info("Initiating Data Ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion Completed")
        
        logging.info("Initiating Data Validation")
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact,data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")
        
        logging.info("Initiating Data transformation")
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data transformation Completed")
        print(data_transformation_artifact)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


if __name__ == "__main__":
    main()
