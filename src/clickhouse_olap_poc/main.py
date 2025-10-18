# -*- coding: utf-8 -*-
import time
from clickhouse_olap_poc.compare_with_mysql import compare_query_performance_with_mysql
from clickhouse_olap_poc.compare_with_postgresql import compare_query_performance_with_postgresql

def main():
    
    print("\n\n" + "="*30)
    print("       C O M P A R I S O N")
    
    ## MySQL vs ClickHouse
    mysql_clickhouse_peformance = compare_query_performance_with_mysql()
    mysql_time = mysql_clickhouse_peformance["mysql_time"]
    clickhouse_time = mysql_clickhouse_peformance["clickhouse_time"]
    print("="*30)
    print(f"MySQL Query Time:      {mysql_time:.4f} seconds")
    print(f"ClickHouse Query Time: {clickhouse_time:.4f} seconds")
    print("-"*30)
    if clickhouse_time > 0:
        improvement = mysql_time / clickhouse_time
        print(f"ClickHouse was {improvement:.1f}x faster than MySQL for this analytical query.")

    print("\n")
    
    ## Postgresql vs ClickHouse
    postgresql_clickhouse_peformance = compare_query_performance_with_postgresql()
    postgresql_time = postgresql_clickhouse_peformance["postgresql_time"]
    clickhouse_time = postgresql_clickhouse_peformance["clickhouse_time"]
    print("="*30)
    print(f"Postgresql Query Time:      {postgresql_time:.4f} seconds")
    print(f"ClickHouse Query Time: {clickhouse_time:.4f} seconds")
    print("-"*30)
    if clickhouse_time > 0:
        improvement = postgresql_time / clickhouse_time
        print(f"ClickHouse was {improvement:.1f}x faster than Postgresql for this analytical query.")
    print("="*30)

if __name__ == "__main__":
    main()