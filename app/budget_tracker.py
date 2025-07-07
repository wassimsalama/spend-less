# app/budget_tracker.py

import pandas as pd

# app/budget_tracker.py

def calculate_budget_summary(df, monthly_budget):
    # Treat Amounts as positive for summing spend
    total_spent = -df["Amount"].sum()

    remaining = monthly_budget - total_spent
    percent_used = round((total_spent / monthly_budget) * 100, 1)

    return {
        "Total Spent": round(total_spent, 2),
        "Remaining": round(remaining, 2),
        "Percent Used": percent_used
    }
