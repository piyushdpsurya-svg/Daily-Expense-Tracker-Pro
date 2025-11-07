import streamlit as st
import pandas as pd

st.set_page_config(page_title="Expense Tracker", page_icon="💸")
st.title("Monthly Expense Tracker")

# single source of truth: a DataFrame
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Amount", "Reason"])

c1, c2 = st.columns(2)
amt = c1.number_input("Amount (₹)", min_value=0.0, step=0.01, format="%.2f")
reason = c2.text_input("Reason")

if st.button("Add"):
    if amt and reason.strip():
        st.session_state.df.loc[len(st.session_state.df)] = [float(amt), reason.strip()]
    else:
        st.warning("Enter both amount and reason.")

if st.button("Show total & reasons"):
    if len(st.session_state.df):
        st.table(st.session_state.df)
        st.metric("Total Expenditure", f"₹{st.session_state.df['Amount'].sum():,.2f}")
    else:
        st.info("No expenses yet.")

left, right = st.columns(2)
with left:
    if st.button("Reset"):
        st.session_state.df = st.session_state.df.iloc[0:0]

with right:
    if len(st.session_state.df):
        csv = st.session_state.df.to_csv(index=False)
        st.download_button("Download CSV", data=csv, file_name="expenses.csv", mime="text/csv")
