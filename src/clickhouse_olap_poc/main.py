# -*- coding: utf-8 -*-
import time
from clickhouse_olap_poc.compare_with_mysql import compare_query_performance_with_mysql
from clickhouse_olap_poc.compare_with_postgresql import compare_query_performance_with_postgresql

def main():
    # compare_query_performance_with_mysql()
    compare_query_performance_with_postgresql()

if __name__ == "__main__":
    main()