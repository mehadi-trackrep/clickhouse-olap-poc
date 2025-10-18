import os
import time
import time
import psycopg2
import pandas as pd
import mysql.connector
from typing import Optional
from typing import Literal, Any, Optional
from clickhouse_driver import Client as ClickHouseClient
from clickhouse_olap_poc.generate_data_by_faker import generate_data


# --- Configuration ---
DB_TYPE = Literal['postgres', 'mysql', 'duckdb', 'clickhouse']

CSV_FILE = 'data/fake_logs.csv'
CHUNK_SIZE = 500_000  # Tune per DB (lower for MySQL, higher for DuckDB/CH)
TOTAL_RECORDS = 50_000_000

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
postgresql_CONFIG = {
    'host': '127.0.0.1',
    'user': 'postgres',
    'password': 'secret',
    'database': DB_NAME,
    'port': 5433
}


def setup_postgresql():
    """Connects to PostgreSQL, creates table, and inserts data."""
    print("\n--- Setting up PostgreSQL ---")
    time.sleep(5) # Wait for PostgreSQL to be ready
    conn = psycopg2.connect(**postgresql_CONFIG)
    cursor = conn.cursor()
    
    print("Creating table...")
    cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME};")
    cursor.execute(f"""
        CREATE TABLE {TABLE_NAME} (
            event_time TIMESTAMP,
            url VARCHAR(255),
            country VARCHAR(10),
            response_time_ms INTEGER
        );
    """)
    
    return conn, cursor


def setup_mysql():
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
    
    
    return conn, cursor


def setup_clickhouse():
    """Connects to ClickHouse, creates table, and inserts data."""
    print("\n--- Setting up ClickHouse ---")
    time.sleep(5) # Wait for ClickHouse to be ready
    client = ClickHouseClient(**CLICKHOUSE_CONFIG)
    
    print("Creating database and table...")
    client.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
    client.execute(f"DROP TABLE IF EXISTS {DB_NAME}.{TABLE_NAME};")

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
    
    return client


def insert_big_data(db_type: DB_TYPE) -> None:
    print(f"\n🚀 Starting ingestion into {db_type.upper()} from {CSV_FILE}")
    
    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(f"CSV not found: {CSV_FILE}")
    
    total_inserted = 0
    start_time = time.time()
    conn, cursor, clickhouse_client = None, None, None
    
    if db_type == 'postgres':
        conn, cursor = setup_postgresql()
    elif db_type == 'mysql':
        conn, cursor = setup_mysql()
    elif db_type == 'clickhouse':
        clickhouse_client = setup_clickhouse()
    elif db_type == 'duckdb':
        ...

    try:
        for chunk_df in pd.read_csv(CSV_FILE, chunksize=CHUNK_SIZE):
            
            rows = chunk_df.values.tolist()  # List of lists
            
            if db_type == 'clickhouse':
                chunk_df['event_time'] = pd.to_datetime(chunk_df['event_time'])
                clickhouse_client.execute(f'INSERT INTO {DB_NAME}.{TABLE_NAME} VALUES', chunk_df.to_dict('records'))
            elif db_type == 'postgres':
                insert_query = f"INSERT INTO {TABLE_NAME} (event_time, url, country, response_time_ms) VALUES (%s, %s, %s, %s)"
                cursor.executemany(insert_query, rows)
                conn.commit()
            elif db_type == 'mysql':
                insert_query = f"INSERT INTO {TABLE_NAME} (event_time, url, country, response_time_ms) VALUES (%s, %s, %s, %s)"
                cursor.executemany(insert_query, rows)
                conn.commit()
            elif db_type == 'duckdb':
                placeholders = ','.join(['?'] * len(chunk_df.columns))
                insert_query = f"INSERT INTO {TABLE_NAME} VALUES ({placeholders})"
                cursor.executemany(insert_query, rows)
                conn.commit()
            
            total_inserted += len(chunk_df)
            elapsed = time.time() - start_time
            rate = total_inserted / elapsed if elapsed > 0 else 0
            print(f"[{db_type}] Inserted {total_inserted:,} / {TOTAL_RECORDS:,} "
                  f"({total_inserted / TOTAL_RECORDS * 100:.1f}%) | "
                  f"{rate:,.0f} rows/sec")

        total_time = time.time() - start_time
        print(f"\n✅ {db_type.upper()} ingestion complete in {total_time:.2f}s "
              f"({TOTAL_RECORDS / total_time:,.0f} rows/sec)")

    finally:
        if db_type in ('postgres', 'mysql'):
            conn.close()
            cursor.close()
        elif db_type == 'clickhouse':
            clickhouse_client.disconnect()
        elif db_type == 'duckdb':
            conn.close()
            if cursor:
                cursor.close()


def setup_db_insert_big_data():
    """Main function to insert data and setup the databases."""
    insert_big_data(db_type='clickhouse')
    # insert_big_data(db_type='postgres')
    # insert_big_data(db_type='mysql')
    # insert_big_data(db_type='duckdb')


def main():
    setup_db_insert_big_data()
    print("\nDatabase setup complete.")
    print("You can now run the comparison script: compare.py")


# --- Main Execution ---
if __name__ == "__main__":
    main()