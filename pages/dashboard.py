import streamlit as st



# Page settings: hide sidebar, wide layout
st.set_page_config(page_title="Dashboard", layout="wide", initial_sidebar_state="collapsed")

# Safety check
if 'data' not in st.session_state:
    st.warning("⚠ Please upload a CSV file first on the homepage.")
    st.stop()

# Load the uploaded data
df = st.session_state['data']

# Title
st.title("📊 What Would You Like to Explore?")
st.markdown("Choose any one of the following options:")

# Layout with two columns
col1, col2 = st.columns(2)

with col1:
    if st.button("Overall Summary", use_container_width=True):
        st.session_state['selected_view'] = 'summary'
        st.switch_page("pages/analysis.py")

    if st.button("Category-wise Spending", use_container_width=True):
        st.session_state['selected_view'] = 'category'
        st.switch_page("pages/analysis.py")

with col2:
    if st.button("Monthly Trends", use_container_width=True):
        st.session_state['selected_view'] = 'monthly'
        st.switch_page("pages/analysis.py")

    if st.button("Weekly Patterns", use_container_width=True):
        st.session_state['selected_view'] = 'weekly'
        st.switch_page("pages/analysis.py")

# Spacer
st.markdown(" ")

# Centered final button
col_left, col_mid, col_right = st.columns([1, 2, 1])
with col_mid:
    if st.button("Savings Suggestions", use_container_width=True):
        st.session_state['selected_view'] = 'savings'
        st.switch_page("pages/analysis.py")
