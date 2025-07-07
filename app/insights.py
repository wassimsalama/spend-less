# app/insights.py

import pandas as pd

# Keywords for basic rule-based categorization
CATEGORIES = {
    "Food & Dining": ["TIM HORTONS", "MCDONALD", "TURKISH", "RESTAURANT", "BUBBLE TEA", "CAFE", "DINER"],
    "Groceries": ["METRO", "WAL-MART", "SUPERMARKET"],
    "Transport": ["LYFT", "PRESTO", "UBER"],
    "Shopping": ["ZARA", "SPORTCHEK", "STAPLES", "UNIQLO"],
    "Services": ["IMMIGRATION", "DRIVE TEST", "BARBERSHOP"],
    "Entertainment": ["OPENAI", "SUBSCR", "NETFLIX"],
    "Other": []
}

def categorize_transaction(description: str) -> str:
    for category, keywords in CATEGORIES.items():
        if any(kw in description.upper() for kw in keywords):
            return category
    return "Other"

def generate_category_insights(df: pd.DataFrame) -> pd.DataFrame:
    df["Category"] = df["Description"].apply(categorize_transaction)
    category_totals = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    total = df["Amount"].sum()

    insights = []
    for category, amount in category_totals.items():
        percent = (amount / total) * 100
        insights.append({
            "Category": category,
            "Amount": round(amount, 2),
            "Percent of Total": round(percent, 1)
        })

    return pd.DataFrame(insights)
