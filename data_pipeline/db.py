"""Create the normalized SQLite schema (categories -> books) and load data."""
import sqlite3

import pandas as pd

SCHEMA = """
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS categories;

CREATE TABLE categories (
    category_id   INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL UNIQUE
);

CREATE TABLE books (
    book_id     INTEGER PRIMARY KEY,
    title       TEXT NOT NULL,
    price_gbp   REAL NOT NULL,
    price_inr   REAL NOT NULL,
    rating      INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    in_stock    INTEGER NOT NULL CHECK (in_stock IN (0, 1)),
    category_id INTEGER NOT NULL REFERENCES categories(category_id)
);
"""


def build_database(df, db_path="books.db"):
    """Rebuild the DB from scratch. Returns the in-memory categories/books
    DataFrames (with ids) so we can compare pd.merge against SQL later."""
    categories_df = (
        pd.DataFrame({"category_name": sorted(df["category"].unique())})
        .reset_index(drop=True)
    )
    categories_df["category_id"] = categories_df.index + 1

    books_df = df.merge(
        categories_df, left_on="category", right_on="category_name"
    ).drop(columns=["category", "category_name"])
    books_df["in_stock"] = books_df["in_stock"].astype(int)
    books_df.insert(0, "book_id", range(1, len(books_df) + 1))

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    categories_df[["category_id", "category_name"]].to_sql(
        "categories", conn, if_exists="append", index=False
    )
    books_df.to_sql("books", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()
    print(f"[db] wrote {len(categories_df)} categories, {len(books_df)} books -> {db_path}")
    return categories_df, books_df


if __name__ == "__main__":
    from scrape import scrape_all
    from clean import clean
    build_database(clean(scrape_all()))