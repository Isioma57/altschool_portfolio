import logging
from config import (
    GOOGLE_APPLICATION_CREDENTIALS, PROJECT_ID, BIGQUERY_DATASET, BIGQUERY_TABLE, CSV_FILE_PATH,
    GCS_BUCKET_NAME, API_ENDPOINT, PROJECT_ID, API_BIGQUERY_DATASET, API_BIGQUERY_TABLE
)
from csv_loader import CsvLoader
from api_loader import ApiLoader

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# Loading CSV file into Bigquery
def load_csv_task() -> None:
    """
    Load a CSV file into a BigQuery table.
    """
    try:
        csv_file_path = CSV_FILE_PATH
        bq_loader = CsvLoader(
            project_id=PROJECT_ID,
            dataset_id=BIGQUERY_DATASET,
            table_id=BIGQUERY_TABLE
        )
        bq_loader.load_csv_to_bigquery(csv_file_path)
        logger.info("CSV file loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading CSV file: {e}")
        
        
        
# Loading to BigQuery
def load_api_task() -> None:
    """
    Fetch data from an API, save it to GCS, and load it into a BigQuery table.
    """
    try:
        api_loader = ApiLoader(
            bucket_name=GCS_BUCKET_NAME,
            api_url=API_ENDPOINT,
            project_id=PROJECT_ID,
            dataset_id=API_BIGQUERY_DATASET,
            table_id=API_BIGQUERY_TABLE
        )
        api_loader.execute()
        logger.info("API data loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading API data: {e}")

        

if __name__ == "__main__":
    load_csv_task()
    load_api_task()
