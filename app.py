import streamlit as st
import dashboard

st.set_page_config(
    page_title="Student Performance Analyzer",
    page_icon="🎓",
    layout="wide"
)

dashboard.show_dashboard()