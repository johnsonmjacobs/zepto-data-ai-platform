"""SQL queries (saved with output) and the read_sql vs merge comparison."""
import sqlite3

import pandas as pd
from pandas.testing import assert_frame_equal

QUERIES = {
    "Q1 SELECT / WHERE - cheap books in stock":
        "SELECT title, price_gbp FROM books WHERE in_stock = 1 AND price_gbp < 20",
    "Q2 ORDER BY + LIMIT - 10 most expensive books":
        "SELECT title, price_gbp, price_inr FROM books ORDER BY price_gbp DESC LIMIT 10",
    "Q3 DISTINCT - rating values present":
        "SELECT DISTINCT rating FROM books ORDER BY rating",
    "Q4 IN - books rated 4 or 5":
        "SELECT title, rating FROM books WHERE rating IN (4, 5) ORDER BY rating DESC, title",
    "Q5 BETWEEN - mid-priced books (GBP 10 to 20)":
        "SELECT title, price_gbp FROM books WHERE price_gbp BETWEEN 10 AND 20 ORDER BY price_gbp",
    "Q6 JOIN + GROUP BY - stats per category":
        """SELECT c.category_name, COUNT(*) AS n_books,
                  ROUND(AVG(b.price_gbp), 2) AS avg_price_gbp,
                  ROUND(AVG(b.rating), 2) AS avg_rating
           FROM books b JOIN categories c ON b.category_id = c.category_id
           GROUP BY c.category_name ORDER BY n_books DESC""",
    "Q7 JOIN + window function - top 10 rated books per category":
        """SELECT category_name, title, rating, price_gbp FROM (
               SELECT c.category_name, b.title, b.rating, b.price_gbp,
                      ROW_NUMBER() OVER (PARTITION BY c.category_name
                                         ORDER BY b.rating DESC, b.title) AS rn
               FROM books b JOIN categories c ON b.category_id = c.category_id
           ) WHERE rn <= 10 ORDER BY category_name, rn""",
}

# Join query used for the pandas equivalence check
JOIN_SQL = """
SELECT c.category_name, b.title, b.rating, b.price_gbp
FROM books b JOIN categories c ON b.category_id = c.category_id
WHERE b.rating >= 4
ORDER BY b.rating DESC, b.price_gbp DESC, b.title
"""


def run_queries(db_path, out_path="query_results.md"):
    conn = sqlite3.connect(db_path)
    lines = ["# SQL query results\n"]
    for name, sql in QUERIES.items():
        result = pd.read_sql(sql, conn)
        print(f"\n--- {name} ---\n{result.head(10).to_string(index=False)}")
        lines.append(f"## {name}\n\n```sql\n{sql.strip()}\n```\n")
        lines.append(f"Rows returned: {len(result)}\n\n```\n{result.to_string(index=False)}\n```\n")
    conn.close()
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\n[queries] saved to {out_path}")


def compare_sql_and_pandas(db_path, categories_df, books_df, out_path="join_comparison.md"):
    conn = sqlite3.connect(db_path)
    sql_df = pd.read_sql(JOIN_SQL, conn)
    conn.close()

    merged = books_df.merge(categories_df, on="category_id")
    pandas_df = (
        merged.loc[merged["rating"] >= 4, ["category_name", "title", "rating", "price_gbp"]]
        .sort_values(["rating", "price_gbp", "title"], ascending=[False, False, True])
        .reset_index(drop=True)
    )

    assert_frame_equal(sql_df, pandas_df)  # raises if they differ
    print("\n[compare] pd.read_sql and pd.merge results are IDENTICAL "
          f"({len(sql_df)} rows)")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# pd.read_sql vs pd.merge\n\n")
        f.write("## read_sql (first 10)\n\n```\n" + sql_df.head(10).to_string() + "\n```\n\n")
        f.write("## merge (first 10)\n\n```\n" + pandas_df.head(10).to_string() + "\n```\n\n")
        f.write(f"`assert_frame_equal` passed: both have {len(sql_df)} rows and identical values.\n")