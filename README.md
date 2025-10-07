

## To get editable python src modules as package:-
- uv pip install --no-deps -e .



## Comparison of MySQL & ClickHouse
1. 
```
--- Setting up MySQL ---
Creating table...
Inserting 1,000,000 records into MySQL (this may take a minute)...
MySQL insert time: 18.91 seconds.

--- Setting up ClickHouse ---
Creating database and table...
Inserting 1,000,000 records into ClickHouse...
ClickHouse insert time: 8.94 seconds.
```


2.
```
==============================
       C O M P A R I S O N
==============================
MySQL Query Time:      0.8984 seconds
ClickHouse Query Time: 0.0452 seconds
------------------------------
ClickHouse was 19.9x faster for this analytical query.
==============================
```


## All in single window

```
--- Running Analytical Query on MySQL ---
Query executed in: 0.8500 seconds.
Top 3 Results:
('/blog', 36258, Decimal('2509'))
('/list', 33738, Decimal('2509'))
('/categories', 33100, Decimal('2500'))

--- Running Analytical Query on ClickHouse ---
Query executed in: 0.0333 seconds.
Top 3 Results:
('/blog', 36258, 2509.0)
('/list', 33738, 2509.0)
('/categories', 33100, 2500.0)

--- Running Analytical Query on postgresql ---
Query executed in: 0.1091 seconds.
Top 3 Results:
('/app', 41853, Decimal('2519'))
('/tag', 33112, Decimal('2511'))
('/blog', 30925, Decimal('2515'))

--- Running Analytical Query on ClickHouse ---
Query executed in: 0.0177 seconds.
Top 3 Results:
('/blog', 36258, 2509.0)
('/list', 33738, 2509.0)
('/categories', 33100, 2500.0)


==============================
       C O M P A R I S O N
==============================
Postgresql Query Time:      0.8500 seconds
ClickHouse Query Time: 0.0333 seconds
------------------------------
ClickHouse was 25.5x faster than MySQL for this analytical query.


==============================
Postgresql Query Time:      0.1091 seconds
ClickHouse Query Time: 0.0177 seconds
------------------------------
ClickHouse was 6.2x faster than Postgresql for this analytical query.
```

