"""Turn the raw scraped strings into properly typed columns."""
import pandas as pd

# Project-defined constant for this assignment. NOT a live market rate.
GBP_TO_INR = 105.50

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def parse_availability(text):
    """True / False for known strings, None for anything unexpected."""
    if not isinstance(text, str):
        return None
    t = text.lower()
    if "out of stock" in t:
        return False
    if "in stock" in t:
        return True
    return None


def clean(raw):
    df = raw.copy()
    n_start = len(df)

    # price: strip the currency symbol -> float (bad values become NaN)
    df["price_gbp"] = pd.to_numeric(
        df["price"].str.replace(r"[^0-9.]", "", regex=True), errors="coerce"
    )
    # rating: text -> int (unknown text becomes NaN)
    df["rating"] = df["star_rating"].map(RATING_MAP)
    # availability text -> boolean (unknown becomes None)
    df["in_stock"] = df["availability"].apply(parse_availability)

    # --- Messy-row policy -------------------------------------------------
    # price_gbp (numeric measurement): median imputation, so one odd price
    #   does not cost us an otherwise good row.
    # title / rating / in_stock: DROP the row. A made-up star rating or stock
    #   flag would be fabricated information, and a book without a title
    #   cannot be identified.
    n_bad_price = int(df["price_gbp"].isna().sum())
    if n_bad_price:
        df["price_gbp"] = df["price_gbp"].fillna(df["price_gbp"].median())

    df = df.dropna(subset=["title", "rating", "in_stock"])
    df = df.drop_duplicates(subset=["title", "category"])

    df["rating"] = df["rating"].astype(int)
    df["in_stock"] = df["in_stock"].astype(bool)

    # fixed baseline conversion: 1 GBP = 105.50 INR
    df["price_inr"] = (df["price_gbp"] * GBP_TO_INR).round(2)

    df = df[["title", "category", "price_gbp", "price_inr", "rating", "in_stock"]]
    df = df.reset_index(drop=True)

    print(f"[clean] rows in: {n_start}, rows out: {len(df)}, "
          f"prices imputed: {n_bad_price}, rows dropped: {n_start - len(df)}")
    return df


if __name__ == "__main__":
    from scrape import scrape_all
    cleaned = clean(scrape_all())
    print(cleaned.dtypes)
    print(cleaned.head())