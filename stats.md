# Clickhouse Stats
# 50M records insertion stats:-

```
[clickhouse] Inserted 500,000 / 50,000,000 (1.0%) | 57,162 rows/sec
...
[clickhouse] Inserted 48,500,000 / 50,000,000 (97.0%) | 98,859 rows/sec
[clickhouse] Inserted 49,000,000 / 50,000,000 (98.0%) | 98,882 rows/sec
[clickhouse] Inserted 49,500,000 / 50,000,000 (99.0%) | 98,888 rows/sec
[clickhouse] Inserted 50,000,000 / 50,000,000 (100.0%) | 98,911 rows/sec
:white_check_mark: CLICKHOUSE ingestion complete in 505.51s (98,910 rows/sec)
```

==============================
       C O M P A R I S O N

--- Running Analytical Query on postgresql ---
Query executed in: 6.1187 seconds.
Top 3 Results:
('/wp-content', 1652995, Decimal('2507'))
('/main', 1651022, Decimal('2509'))
('/tags', 1550548, Decimal('2511'))

--- Running Analytical Query on ClickHouse ---
Query executed in: 0.3479 seconds.
Top 3 Results:
('/wp-content', 1652995, 2507.0)
('/main', 1651022, 2509.0)
('/tags', 1550548, 2511.0)
==============================
Postgresql Query Time:      6.1187 seconds
ClickHouse Query Time: 0.3479 seconds
------------------------------
ClickHouse was 17.6x faster than Postgresql for this analytical query.
==============================

# Postgres Stats
# 50M records insertion stats:-

[postgres] Inserted 48,500,000 / 50,000,000 (97.0%) | 2,353 rows/sec
...
[postgres] Inserted 49,000,000 / 50,000,000 (98.0%) | 2,353 rows/sec
[postgres] Inserted 49,500,000 / 50,000,000 (99.0%) | 2,353 rows/sec
[postgres] Inserted 50,000,000 / 50,000,000 (100.0%) | 2,353 rows/sec

✅ POSTGRES ingestion complete in 21247.35s (2,353 rows/sec)

==============================
       C O M P A R I S O N

--- Running Analytical Query on MySQL ---
Query executed in: 10.3041 seconds.
Top 3 Results:
('/main', 347639, Decimal('2511'))
('/wp-content', 346739, Decimal('2510'))
('/tags', 325540, Decimal('2509'))

--- Running Analytical Query on ClickHouse ---
Query executed in: 0.2497 seconds.
Top 3 Results:
('/wp-content', 1652995, 2507.0)
('/main', 1651022, 2509.0)
('/tags', 1550548, 2511.0)
==============================
MySQL Query Time:      10.3041 seconds
ClickHouse Query Time: 0.2497 seconds
------------------------------
ClickHouse was 41.3x faster than MySQL for this analytical query.


# MySQL Stats
# 50M records insertion stats:-

```
[mysql] Inserted 500,000 / 50,000,000 (1.0%) | 58,640 rows/sec
[mysql] Inserted 1,000,000 / 50,000,000 (2.0%) | 65,148 rows/sec
[mysql] Inserted 1,500,000 / 50,000,000 (3.0%) | 63,810 rows/sec
[mysql] Inserted 2,000,000 / 50,000,000 (4.0%) | 62,759 rows/sec
[mysql] Inserted 2,500,000 / 50,000,000 (5.0%) | 60,667 rows/sec
[mysql] Inserted 3,000,000 / 50,000,000 (6.0%) | 54,797 rows/sec
[mysql] Inserted 3,500,000 / 50,000,000 (7.0%) | 53,839 rows/sec
[mysql] Inserted 4,000,000 / 50,000,000 (8.0%) | 53,924 rows/sec
[mysql] Inserted 4,500,000 / 50,000,000 (9.0%) | 54,119 rows/sec
[mysql] Inserted 5,000,000 / 50,000,000 (10.0%) | 53,736 rows/sec
[mysql] Inserted 5,500,000 / 50,000,000 (11.0%) | 53,786 rows/sec
[mysql] Inserted 6,000,000 / 50,000,000 (12.0%) | 53,625 rows/sec
[mysql] Inserted 6,500,000 / 50,000,000 (13.0%) | 54,115 rows/sec
[mysql] Inserted 7,000,000 / 50,000,000 (14.0%) | 54,787 rows/sec
[mysql] Inserted 7,500,000 / 50,000,000 (15.0%) | 54,894 rows/sec
...
```

==============================
       C O M P A R I S O N


--- Running Analytical Query on MySQL ---
Query executed in: 10.3225 seconds.
Top 3 Results:
('/main', 347639, Decimal('2511'))
('/wp-content', 346739, Decimal('2510'))
('/tags', 325540, Decimal('2509'))

--- Running Analytical Query on ClickHouse ---
Query executed in: 0.2479 seconds.
Top 3 Results:
('/wp-content', 1652995, 2507.0)
('/main', 1651022, 2509.0)
('/tags', 1550548, 2511.0)
==============================
MySQL Query Time:      10.2015 seconds
ClickHouse Query Time: 0.2479 seconds
------------------------------
ClickHouse was 39.7x faster than MySQL for this analytical query.
