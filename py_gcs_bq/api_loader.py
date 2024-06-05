import requests
import os
import json
import logging
from google.cloud import storage, bigquery
from google.api_core.exceptions import NotFound 
from config import GCS_BUCKET_NAME, API_ENDPOINT, PROJECT_ID, API_BIGQUERY_DATASET, API_BIGQUERY_TABLE

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class ApiLoader:
    def __init__(self, bucket_name: str, project_id: str, dataset_id: str, table_id: str, api_url: str):
        """
        Initialize the ApiLoader with GCS bucket, BigQuery dataset and table, and API URL.

        :bucket_name: GCS bucket name
        :project_id: GCP project ID
        :dataset_id: BigQuery dataset ID
        :table_id: BigQuery table ID
        :api_url: API endpoint URL
        """
        self.bucket_name = bucket_name
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.api_url = api_url
        self.storage_client = storage.Client()
        self.bigquery_client = bigquery.Client()

    def fetch_data_from_api(self):
        """
        Fetch data from the API.

        :return: JSON data from the API
        """
        response = requests.get(self.api_url)
        response.raise_for_status()
        logger.info("Fetched data from API")
        return response.json()

    def convert_to_jsonlines(self, data: list):
        """
        Convert a list of JSON records to JSON Lines format.

        :data: List of JSON records
        :return: JSON Lines formatted string
        """
        jsonlines = "\n".join(json.dumps(record) for record in data)
        return jsonlines

    def create_gcs_bucket(self):
        """
        Create a GCS bucket if it does not already exist.
        """
        try:
            self.storage_client.get_bucket(self.bucket_name)
            logger.info(f"GCS bucket {self.bucket_name} already exists.")
        except NotFound:
            bucket = self.storage_client.bucket(self.bucket_name)
            bucket.location = "europe-west1"
            bucket = self.storage_client.create_bucket(bucket)
            logger.info(f"Created GCS bucket {bucket.name}")

    def save_data_to_gcs(self, data: str, gcs_path: str):
        """
        Save data to GCS.

        :data: Data to save
        :gcs_path: GCS path to save the data
        """
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(gcs_path)
        blob.upload_from_string(data, content_type='application/json')
        logger.info(f"Data uploaded to GCS at {gcs_path}")

    def create_bigquery_dataset(self):
        """
        Create a BigQuery dataset if it does not already exist.
        """
        dataset_id = f"{self.project_id}.{self.dataset_id}"
        try:
            self.bigquery_client.get_dataset(dataset_id)
            logger.info(f"Dataset {dataset_id} already exists.")
        except NotFound:
            dataset = bigquery.Dataset(dataset_id)
            dataset.location = "europe-west1"
            self.bigquery_client.create_dataset(dataset)
            logger.info(f"Created dataset {dataset_id}")

    def create_bigquery_table(self, schema_path: str):
        """
        Create a BigQuery table if it does not already exist.

        :schema_path: Path to the table schema file
        """
        table_id = f"{self.project_id}.{self.dataset_id}.{self.table_id}"
        with open(schema_path, 'r') as schema_file:
            schema = json.load(schema_file)
        table = bigquery.Table(table_id, schema=schema)
        try:
            self.bigquery_client.get_table(table_id)
            logger.info(f"Table {table_id} already exists.")
        except NotFound:
            self.bigquery_client.create_table(table)
            logger.info(f"Created table {table_id}")

    def load_json_to_bigquery(self, gcs_uri: str):
        """
        Load JSON Lines data from GCS to BigQuery.

        :gcs_uri: GCS URI of the JSON Lines file
        """
        dataset_ref = self.bigquery_client.dataset(self.dataset_id)
        table_ref = dataset_ref.table(self.table_id)
        job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    autodetect=False,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE  # Ensures table is overwritten
)

        load_job = self.bigquery_client.load_table_from_uri(
            gcs_uri, table_ref, job_config=job_config
        )
        load_job.result()  # Wait for the job to complete
        logger.info(f"Loaded {load_job.output_rows} rows into {self.dataset_id}.{self.table_id}")

    def execute(self):
        """
        Execute the entire pipeline: fetch API data, save to GCS, and load to BigQuery.
        """
        data = self.fetch_data_from_api()
        jsonlines_data = self.convert_to_jsonlines(data)
        gcs_path = 'data/playstation_games.jsonl'
        gcs_uri = f'gs://{self.bucket_name}/{gcs_path}'
        
        self.create_gcs_bucket()
        self.save_data_to_gcs(jsonlines_data, gcs_path)
        
        self.create_bigquery_dataset()
        self.create_bigquery_table(os.path.join(os.path.dirname(__file__), 'schemas', 'schema.json'))
        
        self.load_json_to_bigquery(gcs_uri)

# Ensure GOOGLE_APPLICATION_CREDENTIALS is set
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
