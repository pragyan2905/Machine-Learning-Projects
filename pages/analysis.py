import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Analysis Panel", layout="wide")

if 'data' not in st.session_state or 'selected_view' not in st.session_state:
    st.warning("No data or section selected. Please start from the homepage.")
    st.stop()

df = st.session_state['data']
view = st.session_state['selected_view']

st.title("📊 Expense Insights")

if view == 'summary':
    st.header("📌 Overall Summary")
    total = df['Amount'].sum()
    st.metric(label="💸 Total Spent", value=f"₹{total:,.2f}")
    st.subheader("🔝 Top 5 Transactions")
    top5 = df.sort_values(by='Amount', ascending=False).head(5)
    st.dataframe(top5[['Date', 'Amount', 'Category', 'Description']])
    st.subheader("📂 Spending by Category")
    cat_total = df.groupby('Category')['Amount'].sum().sort_values()
    fig, ax = plt.subplots()
    cat_total.plot(kind='barh', ax=ax, color='skyblue')
    ax.set_xlabel("Total Amount (₹)")
    ax.set_ylabel("Category")
    st.pyplot(fig)

elif view == 'category':
    st.header("📂 Category-wise Spending Analysis")
    category_summary = df.groupby('Category').agg({
        'Amount': ['sum', 'mean', 'count']
    })
    category_summary.columns = ['Total Spent', 'Average Per Transaction', 'Transaction Count']
    st.dataframe(category_summary.sort_values(by='Total Spent', ascending=False))
    st.subheader("🔍 Category-wise Bar Chart")
    fig, ax = plt.subplots()
    category_summary['Total Spent'].sort_values().plot(kind='barh', ax=ax, color='lightgreen')
    ax.set_xlabel("₹ Total")
    st.pyplot(fig)

elif view == 'monthly':
    st.header("📅 Monthly Spending Trends")
    monthly = df.groupby(df['Month'])['Amount'].sum()
    fig, ax = plt.subplots()
    monthly.plot(marker='o', ax=ax, color='tomato')
    ax.set_ylabel("₹ Spent")
    ax.set_xlabel("Month")
    ax.set_title("Spending Over Time")
    st.pyplot(fig)

elif view == 'weekly':
    st.header("📈 Weekly Spending Patterns")
    weekly = df.groupby(df['DayOfWeek'])['Amount'].mean().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ])
    fig, ax = plt.subplots()
    sns.barplot(x=weekly.index, y=weekly.values, ax=ax, palette="coolwarm")
    ax.set_ylabel("₹ Average Spend")
    ax.set_title("Average Spend Per Day")
    st.pyplot(fig)

elif view == 'savings':
    st.header("💡 Savings Suggestions")
    income = st.session_state.get('income', 0)
    goal = st.session_state.get('goal', 0)
    spent = df['Amount'].sum()
    expected = income - goal
    st.write(f"💰 Monthly Income: ₹{income:,.2f}")
    st.write(f"🎯 Savings Goal: ₹{goal:,.2f}")
    st.write(f"📉 Allowable Expenses: ₹{expected:,.2f}")
    st.write(f"💸 Total Spent: ₹{spent:,.2f}")
    if spent <= expected:
        st.success("Great job! You're within your savings target. ✅")
    else:
        overspend = spent - expected
        st.error(f"⚠ You overspent by ₹{overspend:,.2f}")
        cuts = df.groupby('Category')['Amount'].sum().sort_values(ascending=False).head(3)
        st.write("📌 Suggested areas to reduce spending:")
        st.dataframe(cuts)

else:
    st.warning("No valid view selected.")
