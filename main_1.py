import streamlit as st
import pandas as pd

st.set_page_config(page_title="Smart Expense Analyzer", layout="wide")

st.title("💼 Personal Finance Analyzer")
st.subheader("Upload your monthly expenses and set your financial goal.")

st.markdown("### What This App Can Do:")
st.markdown("""
• Analyze your expenses across categories  
• Show trends over time  
• Suggest areas to cut spending  
• Help you reach your savings goals
""")

income = st.number_input("Enter your Monthly Income (₹)", min_value=0)
goal = st.number_input("Enter your Savings Goal (₹)", min_value=0)

uploaded_file = st.file_uploader("Upload your Expense CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if 'Date' in df.columns and 'Amount' in df.columns and 'Category' in df.columns:
        df.dropna(subset=['Date', 'Amount', 'Category'], inplace=True)
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df.dropna(subset=['Amount', 'Date'], inplace=True)
        df['Category'] = df['Category'].str.capitalize().str.strip()
        df['Description'] = df['Description'].fillna("No description")
        df['Month'] = df['Date'].dt.to_period('M').astype(str)
        df['DayOfWeek'] = df['Date'].dt.day_name()

        st.session_state['data'] = df
        st.session_state['income'] = income
        st.session_state['goal'] = goal

        if st.button("Continue to Dashboard"):
            st.switch_page("pages/dashboard.py")
    else:
        st.error("Please make sure the CSV has 'Date', 'Amount', and 'Category' columns.")
