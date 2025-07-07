import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sidebar menu
st.sidebar.title("📂 Menu")
page = st.sidebar.selectbox("Choose a view", [
    "Home",
    "Insights",
    "Budget Summary",
    "Clustering Dashboard"
])

# --------- Clustering Dashboard Page ---------
def clustering_dashboard():
    st.title("📊 Expense Clustering Dashboard")

    try:
        # Load clustered CSV
        df = pd.read_csv("clustered_td.csv")

        # Map cluster numbers to labels
        cluster_labels = {
            0: "Rideshare",
            1: "Retail",
            2: "Transit & Tests",
            3: "Local Cafés & Uni",
            4: "Chain Food & Fitness",
            5: "Misc Local Travel"
        }
        df["Category"] = df["Cluster"].map(cluster_labels)

        # Bar chart of total spending by category
        st.subheader("🧾 Total Spending by Category")
        summary = df.groupby("Category")["Amount"].sum().sort_values()
        st.bar_chart(summary.abs())

        # Filter transactions by category
        selected = st.selectbox("Filter by Category", ["All"] + list(cluster_labels.values()))
        filtered_df = df if selected == "All" else df[df["Category"] == selected]

        # Show transactions
        st.subheader("📋 Transactions")
        st.dataframe(filtered_df[["Date", "Description", "Amount", "Category"]])

    except FileNotFoundError:
        st.error("❌ clustered_td.csv not found. Please make sure you have clustered your transactions first.")

# --------- Home Page ---------
def home_page():
    st.title("🏠 Welcome to SpendLess")
    st.write("""
        Upload your transaction statements and get powerful insights, automatic clustering, and visual analysis to manage your spending.
        
        ✅ Supports PDF → CSV parsing  
        ✅ Auto-categorizes transactions using AI  
        ✅ Tracks your spending patterns over time
    """)

# --------- Placeholder Pages ---------
def insights_page():
    st.title("📈 Insights")
    st.write("This section is under construction.")

def budget_summary_page():
    st.title("💸 Budget Summary")
    st.write("This section is under construction.")

# --------- Router ---------
if page == "Clustering Dashboard":
    clustering_dashboard()
elif page == "Home":
    home_page()
elif page == "Insights":
    insights_page()
elif page == "Budget Summary":
    budget_summary_page()
