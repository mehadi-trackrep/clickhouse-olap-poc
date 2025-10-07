import time
import pandas as pd
import mysql.connector
from typing import Optional
from clickhouse_driver import Client as ClickHouseClient
from clickhouse_olap_poc.generate_data_by_faker import generate_data

# --- Configuration ---
NUM_RECORDS = 1_000_000
DB_NAME = 'demodb'
TABLE_NAME = 'logs'

# --- Database Connection Details ---
# We use the service names from docker-compose as hostnames
CLICKHOUSE_CONFIG = {
    'host': '127.0.0.1',
    'user': 'default',
    'password': 'secret'
}
MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'secret',
    'database': DB_NAME,
    'port': 3310
}


def setup_mysql(data):
    """Connects to MySQL, creates table, and inserts data."""
    print("\n--- Setting up MySQL ---")
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    
    print("Creating table...")
    cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME};")
    cursor.execute(f"""
        CREATE TABLE {TABLE_NAME} (
            event_time DATETIME,
            url VARCHAR(255),
            country VARCHAR(10),
            response_time_ms INT
        ) ENGINE=InnoDB;
    """)
    
    print(f"Inserting {len(data):,} records into MySQL (this may take a minute)...")
    start_time = time.time()
    
    # Convert DataFrame to list of tuples for bulk insert
    tuples = []
    for row in data.itertuples(index=False):
        tuples.append((row.event_time.to_pydatetime(), row.url, row.country, row.response_time_ms))

    insert_query = f"INSERT INTO {TABLE_NAME} (event_time, url, country, response_time_ms) VALUES (%s, %s, %s, %s)"
    cursor.executemany(insert_query, tuples)
    conn.commit() # Important: commit the transaction
    
    end_time = time.time()
    print(f"MySQL insert time: {end_time - start_time:.2f} seconds.")
    
    cursor.close()
    conn.close()


def setup_clickhouse(data):
    """Connects to ClickHouse, creates table, and inserts data."""
    print("\n--- Setting up ClickHouse ---")
    time.sleep(5) # Wait for ClickHouse to be ready
    client = ClickHouseClient(**CLICKHOUSE_CONFIG)
    
    print("Creating database and table...")
    client.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
    client.execute(f"DROP TABLE IF EXISTS {DB_NAME}.{TABLE_NAME};")
    # A database named 'default' already exists. We'll use the one created by MySQL.
    # Note: ORDER BY is the most critical part for ClickHouse performance!
    client.execute(f"""
        CREATE TABLE {DB_NAME}.{TABLE_NAME} (
            event_time DateTime,
            url String,
            country String,
            response_time_ms UInt32
        ) ENGINE = MergeTree()
        ORDER BY (url, event_time);
    """)

    print(f"Inserting {len(data):,} records into ClickHouse...")
    start_time = time.time()
    # The client handles batching efficiently
    client.execute(f'INSERT INTO {DB_NAME}.{TABLE_NAME} VALUES', data.to_dict('records'))
    
    end_time = time.time()
    print(f"ClickHouse insert time: {end_time - start_time:.2f} seconds.")


def setup_db(data: Optional[pd.DataFrame] = None):
    """Main function to insert data and setup the databases."""
    setup_mysql(data)
    setup_clickhouse(data)

def main():
    # Generate data once    
    log_data = generate_data(NUM_RECORDS)
    print(f"Generated {len(log_data):,} records.")
    print(log_data.head())
    
    setup_db(
        data=log_data
    )
    print("\nDatabase setup complete.")
    print("You can now run the comparison script: compare.py")

# --- Main Execution ---
if __name__ == "__main__":
    main()