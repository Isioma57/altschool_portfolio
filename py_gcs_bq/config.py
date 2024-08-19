from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Google Cloud credentials
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Project id
PROJECT_ID = os.getenv('PROJECT_ID')

# Load csv file directly to big query
BIGQUERY_DATASET = os.getenv('BIGQUERY_DATASET')
BIGQUERY_TABLE = os.getenv('BIGQUERY_TABLE')
CSV_FILE_PATH = os.getenv('CSV_FILE_PATH')


# API credentials and settings for loading api data into GCS bucket and BigQuery
GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
API_ENDPOINT = os.getenv('API_ENDPOINT')
API_BIGQUERY_DATASET = os.getenv('API_BIGQUERY_DATASET')
API_BIGQUERY_TABLE = os.getenv('API_BIGQUERY_TABLE')