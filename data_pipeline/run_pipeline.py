"""Run the whole data pipeline: scrape -> clean -> convert -> store -> query."""
from scrape import scrape_all
from clean import clean
from db import build_database
from queries import run_queries, compare_sql_and_pandas

DB_PATH = "books.db"

if __name__ == "__main__":
    raw = scrape_all()
    raw.to_csv("books_raw.csv", index=False)

    cleaned = clean(raw)
    cleaned.to_csv("books_clean.csv", index=False)
    print(cleaned.dtypes)

    categories_df, books_df = build_database(cleaned, DB_PATH)
    run_queries(DB_PATH)
    compare_sql_and_pandas(DB_PATH, categories_df, books_df)