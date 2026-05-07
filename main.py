import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from datetime import datetime
import os

# Create folders
folders = ["data", "outputs", "images", "reports"]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

# ---------------------------------------------------
# CREATE SYNTHETIC DATASET
# ---------------------------------------------------

expense_data = {
    "Date": [
        "2026-01-01", "2026-01-02", "2026-01-03",
        "2026-01-05", "2026-01-07", "2026-01-10",
        "2026-02-01", "2026-02-03", "2026-02-10",
        "2026-03-01", "2026-03-05", "2026-03-10"
    ],
    "Category": [
        "Food", "Transport", "Shopping",
        "Bills", "Entertainment", "Food",
        "Food", "Bills", "Transport",
        "Shopping", "Food", "Bills"
    ],
    "Amount": [
        250, 120, 1500,
        2200, 800, 350,
        400, 2100, 180,
        3200, 450, 2300
    ],
    "Payment_Method": [
        "Cash", "UPI", "Card",
        "UPI", "Cash", "Card",
        "UPI", "Card", "Cash",
        "Card", "UPI", "UPI"
    ],
    "Description": [
        "Lunch", "Bus Fare", "Clothes",
        "Electricity Bill", "Movie",
        "Dinner", "Groceries",
        "Internet Bill", "Taxi",
        "Electronics", "Snacks",
        "Water Bill"
    ]
}

df = pd.DataFrame(expense_data)

# Save CSV
csv_path = "data/expenses.csv"
df.to_csv(csv_path, index=False)

print("Expense dataset created successfully.")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = pd.read_csv(csv_path)

print("\nDataset Preview:")
print(df.head())

# ---------------------------------------------------
# DATA CLEANING
# ---------------------------------------------------

# Convert date column
df["Date"] = pd.to_datetime(df["Date"])

# Remove missing values
df.dropna(inplace=True)

# Remove duplicates
df.drop_duplicates(inplace=True)

# Create Month column
df["Month"] = df["Date"].dt.strftime("%Y-%m")

print("\nData cleaned successfully.")

# ---------------------------------------------------
# STORE DATA IN SQLITE
# ---------------------------------------------------

conn = sqlite3.connect("data/expenses.db")

df.to_sql("expenses", conn, if_exists="replace", index=False)

print("\nData stored in SQLite database.")

# ---------------------------------------------------
# CATEGORY-WISE ANALYSIS
# ---------------------------------------------------

category_analysis = df.groupby("Category")["Amount"].sum()

print("\nCategory-wise Spending:")
print(category_analysis)

# Highest spending category
highest_category = category_analysis.idxmax()
highest_amount = category_analysis.max()

print(f"\nHighest Spending Category: {highest_category}")
print(f"Amount: ₹{highest_amount}")

# ---------------------------------------------------
# MONTHLY ANALYSIS
# ---------------------------------------------------

monthly_analysis = df.groupby("Month")["Amount"].sum()

print("\nMonthly Spending:")
print(monthly_analysis)

# ---------------------------------------------------
# PAYMENT METHOD ANALYSIS
# ---------------------------------------------------

payment_analysis = df.groupby("Payment_Method")["Amount"].sum()

print("\nPayment Method Analysis:")
print(payment_analysis)

# ---------------------------------------------------
# DAILY SPENDING
# ---------------------------------------------------

daily_spending = df.groupby("Date")["Amount"].sum()

average_daily_spending = daily_spending.mean()

print(f"\nAverage Daily Spending: ₹{average_daily_spending:.2f}")

# ---------------------------------------------------
# VISUALIZATION
# ---------------------------------------------------

sns.set_style("whitegrid")

# 1. Category-wise Bar Chart
plt.figure(figsize=(8, 5))
category_analysis.plot(kind="bar")
plt.title("Category-wise Spending")
plt.ylabel("Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("images/category_spending.png")
plt.close()

# 2. Monthly Spending Line Chart
plt.figure(figsize=(8, 5))
monthly_analysis.plot(marker="o")
plt.title("Monthly Spending Trend")
plt.ylabel("Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("images/monthly_trend.png")
plt.close()

# 3. Payment Method Pie Chart
plt.figure(figsize=(7, 7))
payment_analysis.plot(kind="pie", autopct="%1.1f%%")
plt.ylabel("")
plt.title("Payment Method Distribution")
plt.tight_layout()
plt.savefig("images/payment_method.png")
plt.close()

# 4. Daily Spending Trend
plt.figure(figsize=(10, 5))
daily_spending.plot()
plt.title("Daily Spending Trend")
plt.ylabel("Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("images/daily_spending.png")
plt.close()

print("\nCharts generated successfully.")

# ---------------------------------------------------
# REPORT GENERATION
# ---------------------------------------------------

report = {
    "Total Spending": [df["Amount"].sum()],
    "Average Daily Spending": [average_daily_spending],
    "Highest Spending Category": [highest_category],
    "Highest Category Amount": [highest_amount]
}

report_df = pd.DataFrame(report)

report_df.to_csv("reports/expense_summary_report.csv", index=False)

print("\nExpense summary report generated.")

# ---------------------------------------------------
# FINAL OUTPUT
# ---------------------------------------------------

print("\nPROJECT EXECUTED SUCCESSFULLY")