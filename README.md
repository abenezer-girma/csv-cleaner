# CSV Cleaner

A Python tool that turns a messy CSV file into a clean, ready-to-use one.

## The problem
Real business data is messy: extra spaces, mixed upper/lower case, duplicate rows, different date formats, invalid emails, and numbers like "1,200.00" stored as text.

## What it fixes
- Cleans column names (`Signup Date` -> `signup_date`)
- Removes extra spaces and fix name/country capitalization
- Lowercases emails and flags invalid ones
- Keeps only digits (and a leading +) in phone numbers
- Converts mixed date formats to `YYYY-MM-DD`
- Converts money text to real numbers
- Removes rows with no name and duplicate customers
- Prints a cleaning report

## How to run
```
pip install pandas
python clean_csv.py messy_customers.csv clean_customers.csv
```

## Example result
```
  rows_before: 7
  missing_name_removed: 1
  duplicate_emails_removed: 1
  rows_after: 5
  invalid_emails: 0
```

## Tech
Python, pandas, regular expressions
