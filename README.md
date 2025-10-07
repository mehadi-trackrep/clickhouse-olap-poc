

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
