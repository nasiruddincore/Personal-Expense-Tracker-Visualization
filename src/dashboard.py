import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("💰 Personal Expense Tracker Dashboard")
st.markdown("Track, Analyze, and Visualize Personal Expenses")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():
    conn = sqlite3.connect("data/expenses.db")
    query = "SELECT * FROM expenses"
    df = pd.read_sql(query, conn)
    conn.close()

    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.header("Filter Expenses")

categories = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

payment_methods = st.sidebar.multiselect(
    "Select Payment Method",
    options=df["Payment_Method"].unique(),
    default=df["Payment_Method"].unique()
)

filtered_df = df[
    (df["Category"].isin(categories)) &
    (df["Payment_Method"].isin(payment_methods))
]

# ---------------------------------------------------
# KPI METRICS
# ---------------------------------------------------

total_spending = filtered_df["Amount"].sum()
average_spending = filtered_df["Amount"].mean()
highest_expense = filtered_df["Amount"].max()

highest_category = (
    filtered_df.groupby("Category")["Amount"]
    .sum()
    .idxmax()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Spending", f"₹{total_spending:,.2f}")
col2.metric("Average Expense", f"₹{average_spending:,.2f}")
col3.metric("Highest Expense", f"₹{highest_expense:,.2f}")
col4.metric("Top Category", highest_category)

# ---------------------------------------------------
# DATA PREVIEW
# ---------------------------------------------------

st.subheader("📄 Expense Dataset")

st.dataframe(filtered_df)

# ---------------------------------------------------
# CATEGORY-WISE ANALYSIS
# ---------------------------------------------------

st.subheader("📊 Category-wise Spending")

category_analysis = (
    filtered_df.groupby("Category")["Amount"]
    .sum()
    .sort_values(ascending=False)
)

fig1, ax1 = plt.subplots(figsize=(8, 5))

sns.barplot(
    x=category_analysis.index,
    y=category_analysis.values,
    ax=ax1
)

ax1.set_title("Category-wise Spending")
ax1.set_xlabel("Category")
ax1.set_ylabel("Amount")

st.pyplot(fig1)

# ---------------------------------------------------
# MONTHLY TREND
# ---------------------------------------------------

st.subheader("📈 Monthly Spending Trend")

filtered_df["Month"] = filtered_df["Date"].dt.strftime("%Y-%m")

monthly_analysis = (
    filtered_df.groupby("Month")["Amount"]
    .sum()
)

fig2, ax2 = plt.subplots(figsize=(10, 5))

ax2.plot(
    monthly_analysis.index,
    monthly_analysis.values,
    marker="o"
)

ax2.set_title("Monthly Expense Trend")
ax2.set_xlabel("Month")
ax2.set_ylabel("Amount")

st.pyplot(fig2)

# ---------------------------------------------------
# PAYMENT METHOD ANALYSIS
# ---------------------------------------------------

st.subheader("💳 Payment Method Distribution")

payment_analysis = (
    filtered_df.groupby("Payment_Method")["Amount"]
    .sum()
)

fig3, ax3 = plt.subplots(figsize=(7, 7))

ax3.pie(
    payment_analysis.values,
    labels=payment_analysis.index,
    autopct="%1.1f%%"
)

ax3.set_title("Payment Method Usage")

st.pyplot(fig3)

# ---------------------------------------------------
# DAILY SPENDING TREND
# ---------------------------------------------------

st.subheader("📅 Daily Spending Trend")

daily_spending = (
    filtered_df.groupby("Date")["Amount"]
    .sum()
)

fig4, ax4 = plt.subplots(figsize=(10, 5))

ax4.plot(
    daily_spending.index,
    daily_spending.values
)

ax4.set_title("Daily Spending")
ax4.set_xlabel("Date")
ax4.set_ylabel("Amount")

st.pyplot(fig4)

# ---------------------------------------------------
# DOWNLOAD REPORT
# ---------------------------------------------------

st.subheader("⬇ Download Expense Report")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV Report",
    data=csv,
    file_name="expense_report.csv",
    mime="text/csv"
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")
st.markdown("Built using Python, Pandas, SQLite, Matplotlib, Seaborn, and Streamlit")