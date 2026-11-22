"""CSV Cleaner: turns a messy CSV file into a clean one.

Usage: python clean_csv.py messy_customers.csv clean_customers.csv"""
import sys
import pandas as pd

def clean(df):
    report = {"rows_before": len(df)}

    # 1. Clean the column names: "Signup Date" -> "signup_date"
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # 2. Remove extra spaces in all text columns
    for col in ["name", "email", "phone", "country", "signup_date"]:
        df[col] = df[col].str.strip()

    # 3. Make names and countries look the same: "sara tesfaye" -> "Sara Tesfaye"
    df["name"] = df["name"].str.title()
    df["country"] = df["country"].str.title()

    # 4. Emails: lowercase, and mark ones that don't look real
    df["email"] = df["email"].str.lower()
    df["email_valid"] = df["email"].str.match(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", na=False)

    # 5. Phone numbers: keep only digits, (and a leading +)
    df["phone"] = df["phone"].str.replace(r"[^\d+]", "", regex=True)

    # 6. Dates: turn different formats into one format (YYYY-MM-DD)
    df["signup_date"] = df["signup_date"].apply(
        lambda x: pd.to_datetime(x, errors="coerce", format="mixed")
    ).dt.strftime("%Y-%m-%d")

    # 7. Money: remove commas, then turn into numbers
    df["amount"] = pd.to_numeric(
        df["amount"].astype(str).str.replace(",", ""), errors="coerce"
    )

    # 8. Remove rows with no name, then remove duplicate(same email)
    df = df[df["name"].notna() & (df["name"] != "")]
    report["missing_name_removed"] = report["rows_before"] - len(df)
    before_dupes = len(df)
    df = df.drop_duplicates(subset=["email"], keep="first")
    report["duplicate_emails_removed"] = before_dupes - len(df)

    report["rows_after"] = len(df)
    report["invalid_emails"] = int((~df["email_valid"]).sum())
    return df, report

def main():
    if len(sys.argv) != 3:
        print("Usage: python clean_csv.py input.csv output.csv")
        sys.exit(1)

    df = pd.read_csv(sys.argv[1])
    cleaned, report = clean(df)
    cleaned.to_csv(sys.argv[2], index=False)

    print("Cleaning report")
    print("----------------")
    for key, value in report.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()