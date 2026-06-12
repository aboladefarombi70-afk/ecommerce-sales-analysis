"""
clean_data.py
-------------
Cleans the messy e-commerce dataset (ecommerce_sales_dirty.csv) and writes a
tidy version (ecommerce_sales_clean.csv).

Run it from a terminal:
    python clean_data.py

Each section is commented so you can see WHAT problem it fixes and WHY.
"""

import re
import numpy as np
import pandas as pd

RAW_FILE   = "ecommerce_sales_dirty.csv"
CLEAN_FILE = "ecommerce_sales_clean.csv"

# ----------------------------------------------------------------------
# 1. LOAD
#    dtype=str -> read everything as text first so pandas doesn't guess
#    types on dirty columns. We convert to numbers ourselves later.
# ----------------------------------------------------------------------
df = pd.read_csv(RAW_FILE, dtype=str)
print("Loaded:", df.shape)

# ----------------------------------------------------------------------
# 2. DROP FULLY-EMPTY ROWS, then strip whitespace from every cell
# ----------------------------------------------------------------------
df = df.dropna(how="all")                                   # rows where all cells are NaN
df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
# turn empty strings / common null-words into real NaN
df = df.replace(r"^\s*$", np.nan, regex=True)
df = df.replace(["N/A", "n/a", "NA", "null", "None", "none", "-", "TBD"], np.nan)
# drop rows that became empty after cleaning (only an Order_ID, etc. is your call;
# here we drop rows missing the essentials needed for analysis)

# ----------------------------------------------------------------------
# 3. TEXT STANDARDISATION
# ----------------------------------------------------------------------
def clean_text(s):
    """Remove stray special characters and collapse double spaces."""
    if pd.isna(s):
        return s
    s = re.sub(r"[#@*%&!~^$]", "", str(s))   # strip junk symbols
    s = re.sub(r"\s+", " ", s).strip()        # collapse whitespace
    return s

for col in ["Customer_Name", "City", "Product_Name"]:
    df[col] = df[col].apply(clean_text)

# Names & cities -> Title Case (Lagos, New York). Names with real typos can't be
# "corrected" automatically, so we only standardise casing/whitespace.
df["Customer_Name"] = df["Customer_Name"].str.title()
df["City"]          = df["City"].str.title()

# ----------------------------------------------------------------------
# 4. GENDER  ->  Male / Female / Other
# ----------------------------------------------------------------------
gender_map = {
    "m": "Male", "male": "Male",
    "f": "Female", "female": "Female",
}
df["Gender"] = (df["Gender"].str.strip().str.lower()
                .map(gender_map).fillna(df["Gender"]))
df.loc[~df["Gender"].isin(["Male", "Female"]), "Gender"] = "Other"
df.loc[df["Gender"].isna(), "Gender"] = np.nan  # keep true missing as missing

# ----------------------------------------------------------------------
# 5. COUNTRY  ->  one canonical name each
# ----------------------------------------------------------------------
country_map = {
    "nigeria": "Nigeria", "nigeira": "Nigeria",
    "usa": "USA", "united states": "USA", "us": "USA", "u.s.a": "USA",
    "uk": "UK", "united kingdom": "UK", "u.k": "UK", "england": "UK",
    "india": "India", "inida": "India",
    "canada": "Canada", "canda": "Canada",
    "germany": "Germany", "deutschland": "Germany",
}
df["Country"] = (df["Country"].str.strip().str.lower()
                 .map(country_map).fillna(df["Country"].str.title()))

# ----------------------------------------------------------------------
# 6. PRODUCT_CATEGORY  ->  4 canonical categories
# ----------------------------------------------------------------------
def map_category(x):
    if pd.isna(x):
        return np.nan
    t = re.sub(r"[^a-z]", "", str(x).lower())   # keep letters only: "home-appliances"->"homeappliances"
    if t.startswith("electron"):
        return "Electronics"
    if t.startswith("fash") or t == "clothing":
        return "Fashion"
    if "appliance" in t:
        return "Home Appliances"
    if t.startswith("beauty"):
        return "Beauty Products"
    return np.nan
df["Product_Category"] = df["Product_Category"].apply(map_category)

# ----------------------------------------------------------------------
# 7. PAYMENT_METHOD  ->  consistent labels
# ----------------------------------------------------------------------
def map_payment(x):
    if pd.isna(x):
        return np.nan
    t = re.sub(r"[^a-z]", "", str(x).lower())   # "Credit-Card"/"credit_card"/"CC" -> letters only
    if t in ("creditcard", "cc"):
        return "Credit Card"
    if t in ("debitcard", "dc"):
        return "Debit Card"
    if "paypal" in t:
        return "PayPal"
    if "banktransfer" in t or "wiretransfer" in t:
        return "Bank Transfer"
    if "cashondelivery" in t or t == "cod" or t == "cash":
        return "Cash on Delivery"
    if "applepay" in t:
        return "Apple Pay"
    return x
df["Payment_Method"] = df["Payment_Method"].apply(map_payment)

# ----------------------------------------------------------------------
# 8. NUMERIC COLUMNS  (strip currency symbols, coerce, fix impossibles)
# ----------------------------------------------------------------------
def to_number(s):
    """Remove currency symbols/commas/spaces, then convert to float. Junk -> NaN."""
    if pd.isna(s):
        return np.nan
    s = re.sub(r"[^\d.\-]", "", str(s))         # keep digits, dot, minus
    try:
        return float(s)
    except ValueError:
        return np.nan

df["Unit_Price"] = df["Unit_Price"].apply(to_number)
df["Quantity"]   = df["Quantity"].apply(to_number)
df["Age"]        = df["Age"].apply(to_number)

# Age: anything <=0 or >120 is impossible -> NaN
df.loc[(df["Age"] <= 0) | (df["Age"] > 120), "Age"] = np.nan
df["Age"] = df["Age"].round().astype("Int64")   # nullable integer

# Quantity: 0 or negative is impossible -> NaN. (Huge values kept as outliers to inspect.)
df.loc[df["Quantity"] <= 0, "Quantity"] = np.nan

# Negative unit prices are impossible -> NaN
df.loc[df["Unit_Price"] < 0, "Unit_Price"] = np.nan

# ----------------------------------------------------------------------
# 9. DISCOUNT  ->  decimal fraction between 0 and 1  (10% -> 0.10, "10" -> 0.10)
# ----------------------------------------------------------------------
def to_fraction(s):
    if pd.isna(s):
        return 0.0                               # treat missing discount as none
    v = to_number(s)
    if pd.isna(v):
        return 0.0
    if v > 1:                                    # "10" or "10%" means 10 percent
        v = v / 100.0
    if v < 0 or v > 0.95:                         # clamp nonsense
        return 0.0
    return round(v, 4)
df["Discount"] = df["Discount"].apply(to_fraction)

# ----------------------------------------------------------------------
# 10. TOTAL_SALES  ->  recompute correctly = Quantity * Unit_Price * (1 - Discount)
#     (the raw file had wrong totals in ~10% of rows)
# ----------------------------------------------------------------------
df["Total_Sales"] = (df["Quantity"] * df["Unit_Price"] * (1 - df["Discount"])).round(2)

# ----------------------------------------------------------------------
# 11. CUSTOMER_RATING  ->  numeric, keep only 1..5
# ----------------------------------------------------------------------
df["Customer_Rating"] = df["Customer_Rating"].apply(to_number)
df.loc[(df["Customer_Rating"] < 1) | (df["Customer_Rating"] > 5), "Customer_Rating"] = np.nan

# ----------------------------------------------------------------------
# 12. EMAIL  ->  flag invalid addresses (then blank them out)
# ----------------------------------------------------------------------
email_re = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
def valid_email(s):
    return bool(email_re.match(str(s))) if pd.notna(s) else False
df["Email_Valid"] = df["Customer_Email"].apply(valid_email)
df.loc[~df["Email_Valid"], "Customer_Email"] = np.nan

# ----------------------------------------------------------------------
# 13. ORDER_DATE  ->  parse many formats into one ISO date (YYYY-MM-DD)
#     NOTE: dd/mm/yyyy vs mm/dd/yyyy is genuinely ambiguous. We try day-first
#     first, then month-first for whatever is left. Real projects resolve this
#     with domain knowledge; document the choice you make.
# ----------------------------------------------------------------------
parsed = pd.to_datetime(df["Order_Date"], errors="coerce", dayfirst=True, format="mixed")
mask = parsed.isna() & df["Order_Date"].notna()
parsed.loc[mask] = pd.to_datetime(df.loc[mask, "Order_Date"], errors="coerce", format="mixed")
df["Order_Date"] = parsed.dt.strftime("%Y-%m-%d")

# ----------------------------------------------------------------------
# 14. DUPLICATES  ->  drop exact duplicate rows
# ----------------------------------------------------------------------
before = len(df)
df = df.drop_duplicates()
print("Removed", before - len(df), "duplicate rows")

# ----------------------------------------------------------------------
# 15. ORDER_ID  ->  fill missing ids so every row is identifiable
# ----------------------------------------------------------------------
missing_id = df["Order_ID"].isna()
df.loc[missing_id, "Order_ID"] = ["GEN-" + str(i) for i in range(missing_id.sum())]

# ----------------------------------------------------------------------
# 16. SAVE
# ----------------------------------------------------------------------
df = df.reset_index(drop=True)
df.to_csv(CLEAN_FILE, index=False)
print("Saved:", df.shape, "->", CLEAN_FILE)
print(df.dtypes)
