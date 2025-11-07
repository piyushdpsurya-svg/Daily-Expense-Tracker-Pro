import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Expense Tracker", page_icon="💸")
st.title("Monthly Expense Tracker")

# Keep all expenses in one DataFrame
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Date", "Amount", "Reason"])

# Input fields
c1, c2, c3 = st.columns(3)
exp_date = c1.date_input("Date", value=date.today())
amt = c2.number_input("Amount (₹)", min_value=0.0, step=0.01, format="%.2f")
reason = c3.text_input("Reason")

# Add new entry
if st.button("Add Expense"):
    if amt and reason.strip():
        st.session_state.df.loc[len(st.session_state.df)] = [exp_date, float(amt), reason.strip()]
    else:
        st.warning("Please enter both amount and reason.")

# Show summary
if st.button("Show Summary"):
    if len(st.session_state.df):
        st.table(st.session_state.df)
        total = st.session_state.df["Amount"].sum()
        st.metric("Total Expenditure", f"₹{total:,.2f}")
    else:
        st.info("No expenses recorded yet.")

# Reset and download options
c4, c5 = st.columns(2)
with c4:
    if st.button("Reset All"):
        st.session_state.df = st.session_state.df.iloc[0:0]

with c5:
    if len(st.session_state.df):
        csv = st.session_state.df.to_csv(index=False)
        st.download_button("Download CSV", data=csv, file_name="expenses.csv", mime="text/csv")
