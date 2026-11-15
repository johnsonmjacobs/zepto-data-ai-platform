# Module 1 - Data Pipeline

Scrapes books.toscrape.com, cleans the data, stores it in a normalized SQLite
database and queries it with SQL and pandas.

## Setup and run

    cd data_pipeline
    pip install -r requirements.txt
    python run_pipeline.py

This module has its own `requirements.txt`. 

On a corporate network thatintercepts HTTPS, `truststore`  makes Python use the Windowscertificate store.

Outputs: `books_raw.csv`, `books_clean.csv`, `books.db`, `query_results.md`,
`join_comparison.md`. `books.db` is rebuilt from scratch on every pipeline run - Full Load.

## Scope
4 categories (Travel, Mystery, Historical Fiction, Science Fiction), all
paginated pages: 85 books (11 + 32 + 26 + 16).

## Currency conversion
Fixed project rate: **1 GBP = 105.50 INR**. This is an assignment-defined constant, not using current market rate Hence no API is used.

## Cleaning decisions
- price_gbp: [explain regex + float, and why median imputation]
- rating: [explain mapping and why dropping the row]
- in_stock: [explain the boolean parsing]
- In this run, 0 values were imputed and 0 rows dropped.

## Schema
[describe categories 1---N books, PK/FK, PRAGMA foreign_keys, CHECK rules]

## Queries
[list which query covers which clause: WHERE, ORDER BY, LIMIT, DISTINCT,
IN, BETWEEN, JOIN]. Full output is in `query_results.md`.

## SQL vs pandas
[say that read_sql and merge gave identical results, 32 rows, checked with
assert_frame_equal. See `join_comparison.md`.]