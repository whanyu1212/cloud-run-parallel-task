import os
import pandas as pd
from google.cloud import bigquery
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "./fleet-anagram-244304-449e515c8d17.json"
)

# Initialize clients
bq_client = bigquery.Client()
storage_client = storage.Client()


def process_batch(batch_start, batch_size):
    """Queries a batch of data, processes it, and writes it back."""
    try:
        query = f"""
            SELECT *
            FROM `bigquery-public-data.covid19_open_data.covid19_open_data`
            LIMIT {batch_size} OFFSET {batch_start}
        """
        # Alternatively, if you want to split the batches by identifier, you can do the following:
        # batch_keys = key_identifiers[batch_start:batch_start + batch_size]
        # keys_string = ','.join([f"'{key}'" for key in batch_keys])

        # query = f"""
        #     SELECT *
        #     FROM `bigquery-public-data.covid19_open_data.covid19_open_data`
        #     WHERE key IN ({keys_string})
        # """

        query_job = bq_client.query(query)
        df = query_job.to_dataframe()

        df["processed_value"] = df["new_recovered"] * 2  # Example processing

        df.to_gbq(
            destination_table="fleet-anagram-244304.ml_datasets.test_cloudrun",  # Replace with your table
            project_id="fleet-anagram-244304",
            if_exists="append",
            chunksize=10000,
        )
        print(f"Batch {batch_start} processed and written.")
        return f"Batch {batch_start} successful"
    except Exception as e:
        print(f"Batch {batch_start} error: {e}")
        raise e


def main(event=None):
    task_num = int(os.environ.get("TASK_NUM", 0))
    batch_size = 10000
    batch_start = task_num * batch_size

    result = process_batch(batch_start, batch_size)
    print(f"Task {task_num}: {result}")


if __name__ == "__main__":  # For local testing
    for i in range(2):
        os.environ["TASK_NUM"] = str(i)
        main()
