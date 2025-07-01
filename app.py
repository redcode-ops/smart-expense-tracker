import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Expensify Lite", page_icon="💸")

st.title("💸 Smart Expense Tracker")

# Session state to keep data
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# Form to add expense
with st.form("Add Expense"):
    col1, col2 = st.columns([3, 1])
    with col1:
        note = st.text_input("📝 What did you spend on?")
    with col2:
        amount = st.number_input("₹ Amount", min_value=1.0, step=0.5)

    category = st.selectbox("📁 Category", ["Food", "Travel", "Shopping", "Bills", "Health", "Other"])
    submitted = st.form_submit_button("Add")

    if submitted and note and amount:
        st.session_state.expenses.append({
            "Note": note,
            "Amount": amount,
            "Category": category,
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Time": datetime.now().strftime("%H:%M:%S")
        })
        st.success("Added expense!")

# Search box
search = st.text_input("🔎 Search by keyword")
if search:
    filtered = [e for e in st.session_state.expenses if search.lower() in e["Note"].lower()]
else:
    filtered = st.session_state.expenses

# Show table
if filtered:
    df = pd.DataFrame(filtered)
    st.write("🧾 **Your Expenses**")
    st.dataframe(df, use_container_width=True)

    # Total
    total = sum(e["Amount"] for e in filtered)
    st.metric("💰 Total Spent", f"₹{total:.2f}")

    # Category-wise chart
    cat_df = df.groupby("Category")["Amount"].sum().reset_index()
    st.subheader("📊 Spend by Category")
    st.bar_chart(cat_df, x="Category", y="Amount")

    # Download button
    csv = df.to_csv(index=False).encode()
    st.download_button("⬇️ Download as CSV", data=csv, file_name="expenses.csv", mime="text/csv")
else:
    st.info("No expenses yet.")


