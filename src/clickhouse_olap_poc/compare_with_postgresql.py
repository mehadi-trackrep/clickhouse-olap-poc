import time
from clickhouse_driver import Client as ClickHouseClient
import psycopg2 as postgresql

# --- Configuration ---
DB_NAME = 'demodb'
TABLE_NAME = 'logs'

# --- Database Connection Details ---
# We use the service names from docker-compose as hostnames
CLICKHOUSE_CONFIG = {
    'host': '127.0.0.1',
    'user': 'default',
    'password': 'secret'
}
postgresql_CONFIG = {
    'host': '127.0.0.1',
    'user': 'postgres',
    'password': 'secret',
    'database': DB_NAME,
    'port': 5433
}

# --- The Query to Compare ---
ANALYTICAL_QUERY = f"""
    SELECT
        url,
        COUNT(*) AS visit_count,
        ROUND(AVG(response_time_ms)) AS avg_response_time
    FROM {TABLE_NAME}
    GROUP BY url
    ORDER BY visit_count DESC
    LIMIT 10;
"""

def run_query(db_type, query):
    """Runs the analytical query and times it."""
    print(f"\n--- Running Analytical Query on {db_type} ---")
    
    conn = None
    start_time = time.time()
    
    if db_type == "postgresql":
        conn = postgresql.connect(**postgresql_CONFIG)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
    else: # ClickHouse
        conn = ClickHouseClient(**CLICKHOUSE_CONFIG, database=DB_NAME)
        results = conn.execute(query)

    end_time = time.time()
    
    print(f"Query executed in: {end_time - start_time:.4f} seconds.")
    print("Top 3 Results:")
    for row in results[:3]:
        print(row)
        
    # if conn:
    #     conn.close()
    return end_time - start_time


def compare_query_performance_with_postgresql() -> dict:
    """Compares the performance of the analytical query on both databases."""
    postgresql_time = run_query("postgresql", ANALYTICAL_QUERY)
    clickhouse_time = run_query("ClickHouse", ANALYTICAL_QUERY)
    
    return {
        "postgresql_time": postgresql_time,
        "clickhouse_time": clickhouse_time
    }

# --- 4. Main Execution ---
if __name__ == "__main__":
    # Run the comparison
    compare_query_performance_with_postgresql()