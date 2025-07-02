# Expensify Lite with TinyDB – Cross-Device Login + Persistent Storage

import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import os
from tinydb import TinyDB, Query

# -------------------------
# Page Setup
# -------------------------
st.set_page_config(page_title="Expensify Lite", page_icon="💸")

india_timezone = pytz.timezone('Asia/Kolkata')
now = datetime.now(india_timezone)

# -------------------------
# TinyDB Setup
# -------------------------
os.makedirs("data", exist_ok=True)
db = TinyDB("data/db.json")
users_table = db.table("users")
feedback_table = db.table("feedback")
expenses_table = db.table("expenses")
User = Query()

# -------------------------
# Session State
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.expenses = []

# -------------------------
# LOGIN & SIGNUP SYSTEM
# -------------------------
if not st.session_state.logged_in:
    st.title("🔐 Expensify Lite Login / Signup")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        email = st.text_input("Email").strip().lower()
        password = st.text_input("Password", type="password").strip()

        if st.button("Login"):
            user = users_table.get(User.email == email)
            if user:
                if user["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.user = email
                    # Load previous expenses
                    user_expenses = expenses_table.search(User.email == email)
                    st.session_state.expenses = user_expenses[0]["data"] if user_expenses else []
                    st.success("✅ Logged in successfully!")
                    st.rerun()
                else:
                    st.error("❌ Incorrect password")
            else:
                st.error("❌ Email not registered")

    with tab2:
        new_email = st.text_input("New Email").strip().lower()
        new_password = st.text_input("New Password", type="password").strip()

        if st.button("Sign Up"):
            if users_table.get(User.email == new_email):
                st.warning("⚠️ Email already registered. Please login.")
            elif not new_email or not new_password:
                st.warning("⚠️ Please fill both fields.")
            else:
                users_table.insert({"email": new_email, "password": new_password})
                st.success("✅ Account created! Please login.")

    st.stop()

# -------------------------
# MAIN APP UI
# -------------------------
st.title("💸 Expensify Lite")
st.markdown(f"**👤 Logged in as:** `{st.session_state.user}`")
st.markdown(f"**📅 Date:** {now.strftime('%d-%m-%Y')}  |  🕒 Time:** {now.strftime('%I:%M:%S %p')}")

# -------------------------
# Add Expense
# -------------------------
with st.form("Add Expense"):
    col1, col2 = st.columns([3, 1])
    with col1:
        note = st.text_input("📝 What did you spend on?")
    with col2:
        amount = st.number_input("₹ Amount", min_value=1.0, step=0.5)
    category = st.selectbox("📁 Category", ["Food", "Travel", "Shopping", "Bills", "Health", "Other"])
    submitted = st.form_submit_button("Add")

    if submitted and note and amount:
        entry = {
            "Note": note,
            "Amount": amount,
            "Category": category,
            "Date": now.strftime("%Y-%m-%d"),
            "Time": now.strftime("%I:%M:%S %p")
        }
        st.session_state.expenses.append(entry)
        st.success("✅ Expense added!")
        # Save to TinyDB
        existing = expenses_table.get(User.email == st.session_state.user)
        if existing:
            expenses_table.update({"data": st.session_state.expenses}, User.email == st.session_state.user)
        else:
            expenses_table.insert({"email": st.session_state.user, "data": st.session_state.expenses})

# -------------------------
# Expense Search & Display
# -------------------------
search = st.text_input("🔎 Search your expenses")
if search:
    filtered = [e for e in st.session_state.expenses if search.lower() in e["Note"].lower()]
else:
    filtered = st.session_state.expenses

if filtered:
    df = pd.DataFrame(filtered)
    st.write("🧾 **Your Expenses**")
    st.dataframe(df, use_container_width=True)

    total = sum(e["Amount"] for e in filtered)
    st.metric("💰 Total Spent", f"₹{total:.2f}")

    cat_df = df.groupby("Category")["Amount"].sum().reset_index()
    st.subheader("📊 Spend by Category")
    st.bar_chart(cat_df, x="Category", y="Amount")

    df["Date"] = pd.to_datetime(df["Date"])
    daily = df.groupby(df["Date"].dt.date)["Amount"].sum().reset_index()
    st.subheader("🗓️ Daily Spend Summary")
    st.dataframe(daily, use_container_width=True)
    st.bar_chart(daily, x="Date", y="Amount")

    df["Month"] = df["Date"].dt.strftime('%B %Y')
    monthly = df.groupby("Month")["Amount"].sum().reset_index()
    st.subheader("📆 Monthly Spend Summary")
    st.dataframe(monthly, use_container_width=True)
    st.bar_chart(monthly, x="Month", y="Amount")

    csv = df.to_csv(index=False).encode()
    st.download_button("⬇️ Download CSV", data=csv,
                       file_name=f"{st.session_state.user}_expenses.csv",
                       mime="text/csv")
else:
    st.info("No expenses yet.")

# -------------------------
# Feedback
# -------------------------
st.markdown("---")
st.subheader("💬 Got Feedback?")
with st.form("Feedback"):
    fb = st.text_area("Share your thoughts:", placeholder="This app is cool but could improve if...")
    send = st.form_submit_button("Send Feedback")
    if send and fb:
        feedback_table.insert({
            "email": st.session_state.user,
            "feedback": fb,
            "time": now.strftime("%Y-%m-%d %I:%M:%S %p")
        })
        st.success("✅ Thanks for your feedback!")

# -------------------------
# Logout
# -------------------------
st.sidebar.title("🔓 Logout")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.expenses = []
    st.rerun()
    
 
        
           

  
    
