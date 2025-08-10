import os
import numpy as np
import pandas as pd
import sys

"""
Defining some common constant variables
"""
TARGET_COLUMN = "Result"
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACT_DIR:str = "Artifacts"
FILE_NAME:str = "PhisingData.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"


"""
Data Ingestion related constants, starting with DATA_INGESTION
"""
DATA_INGESTION_COLLECTION_NAME:str = "NetworkData"
DATA_INGESTION_DATABASE_NAME:str = "Ambuj"
DATA_INGESTION_DIR_NAME:str = "data_ingesion"
DATA_INGESTION_FEATURE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2
 