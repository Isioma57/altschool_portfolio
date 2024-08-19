import os
import logging
from google.cloud import bigquery

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class CsvLoader:
    def __init__(self, project_id: str, dataset_id: str, table_id: str):
        """
        Initialize the CsvLoader with project, dataset, and table information.

        project_id: GCP project ID
        dataset_id: BigQuery dataset ID
        table_id: BigQuery table ID
        """
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.client = bigquery.Client()

    def create_dataset(self) -> None:
        """
        Create a BigQuery dataset if it does not already exist.
        """
        dataset_id = f"{self.project_id}.{self.dataset_id}"
        try:
            self.client.get_dataset(dataset_id)
            logger.info(f"Dataset {dataset_id} already exists.")
        except Exception:
            # If dataset does not exist, create it
            dataset = bigquery.Dataset(dataset_id)
            dataset.location = "europe-west1"
            dataset = self.client.create_dataset(dataset)
            logger.info(f"Created dataset {self.client.project}.{dataset.dataset_id}")

    def load_csv_to_bigquery(self, csv_file_path: str) -> None:
        """
        Load a CSV file into a BigQuery table.

        csv_file_path: Path to the CSV file
        """
        self.create_dataset()  # Ensure the dataset exists before loading data
        table_id = f"{self.project_id}.{self.dataset_id}.{self.table_id}"

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            autodetect=True,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE  # if the table already exists, ensure it is overwritten
        )

        with open(csv_file_path, 'rb') as file:
            job = self.client.load_table_from_file(file, table_id, job_config=job_config)
            job.result()  # Wait for the job to complete

        table = self.client.get_table(table_id)
        logger.info(f"Loaded {table.num_rows} rows to {table_id}")

# Ensure GOOGLE_APPLICATION_CREDENTIALS is set
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
