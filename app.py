# Expensify Lite v2 – Smart Expense Tracker with Secure Manual Login + Daily/Monthly Summary + CSV Save + User Tracker

import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import os

# -------------------------
# Page Setup
# -------------------------
st.set_page_config(page_title="Expensify Lite", page_icon="💸")

# Timezone: India Standard Time
india_timezone = pytz.timezone('Asia/Kolkata')
now = datetime.now(india_timezone)

# -------------------------
# Session State Setup
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.expenses = []

# Dummy user database (replace with secure DB or OAuth later)
users_db = {
    "zaina@gmail.com": "zaina123",
    "test@example.com": "test123"
}

# -------------------------
# LOGIN PAGE
# -------------------------
if not st.session_state.logged_in:
    st.title("🔐 Login to Expensify Lite")

    email = st.text_input("Email").strip()
    password = st.text_input("Password", type="password").strip()

    if st.button("Login"):
        if email in users_db:
            if password == users_db[email]:
                st.session_state.logged_in = True
                st.session_state.user = email

                # Load previous data if exists
                file_path = f"expenses/{email.replace('@', '_at_')}.csv"
                if os.path.exists(file_path):
                    st.session_state.expenses = pd.read_csv(file_path).to_dict("records")
                else:
                    st.session_state.expenses = []

                # User tracking log
                user_log_path = "users/expensify_users.csv"
                os.makedirs("users", exist_ok=True)

                login_data = {
                    "Email": email,
                    "Login Time": now.strftime("%Y-%m-%d %I:%M:%S %p"),
                    "Total Expenses": len(st.session_state.expenses),
                    "Last Updated": now.strftime("%Y-%m-%d")
                }

                if os.path.exists(user_log_path):
                    user_df = pd.read_csv(user_log_path)
                    user_df = user_df[user_df["Email"] != email]  # Remove old entry
                    user_df = pd.concat([user_df, pd.DataFrame([login_data])], ignore_index=True)
                else:
                    user_df = pd.DataFrame([login_data])

                user_df.to_csv(user_log_path, index=False)

                st.success(f"✅ Welcome, {email}")
                st.rerun()
            else:
                st.error("❌ Incorrect password")
        else:
            st.error("❌ Email not found")

    st.stop()

# -------------------------
# MAIN APP AFTER LOGIN
# -------------------------
st.title("💸 Expensify Lite")
st.markdown(f"**👤 Logged in as:** `{st.session_state.user}`")
st.markdown(f"**📅 Date:** {now.strftime('%d-%m-%Y')}")
st.markdown(f"**🕒 Time (IST):** {now.strftime('%I:%M:%S %p')}")

# -------------------------
# Add Expense Form
# -------------------------
file_path = f"expenses/{st.session_state.user.replace('@', '_at_')}.csv"

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
            "Date": now.strftime("%Y-%m-%d"),
            "Time": now.strftime("%I:%M:%S %p")
        })
        st.success("✅ Expense added!")

        # Save to CSV
        df_all = pd.DataFrame(st.session_state.expenses)
        os.makedirs("expenses", exist_ok=True)
        df_all.to_csv(file_path, index=False)

# -------------------------
# Filter & Search
# -------------------------
search = st.text_input("🔎 Search your expenses")
if search:
    filtered = [e for e in st.session_state.expenses if search.lower() in e["Note"].lower()]
else:
    filtered = st.session_state.expenses

# -------------------------
# Display Table & Charts
# -------------------------
if filtered:
    df = pd.DataFrame(filtered)
    st.write("🧳️ **Your Expenses**")
    st.dataframe(df, use_container_width=True)

    total = sum(e["Amount"] for e in filtered)
    st.metric("💰 Total Spent", f"₹{total:.2f}")

    cat_df = df.groupby("Category")["Amount"].sum().reset_index()
    st.subheader("📊 Spend by Category")
    st.bar_chart(cat_df, x="Category", y="Amount")

    # --- DAILY SPEND SUMMARY ---
    df["Date"] = pd.to_datetime(df["Date"])
    daily = df.groupby(df["Date"].dt.date)["Amount"].sum().reset_index()
    st.subheader("🗓️ Daily Spend Summary")
    st.dataframe(daily, use_container_width=True)
    st.bar_chart(daily, x="Date", y="Amount")

    # --- MONTHLY SPEND SUMMARY ---
    df["Month"] = df["Date"].dt.strftime('%B %Y')
    monthly = df.groupby("Month")["Amount"].sum().reset_index()
    st.subheader("📆 Monthly Spend Summary")
    st.dataframe(monthly, use_container_width=True)
    st.bar_chart(monthly, x="Month", y="Amount")

    # --- DOWNLOAD BUTTON ---
    csv = df.to_csv(index=False).encode()
    st.download_button("⬇️ Download CSV", data=csv,
                       file_name=f"{st.session_state.user}_expenses.csv",
                       mime="text/csv")
else:
    st.info("No expenses yet.")

# -------------------------
# Logout
# -------------------------
st.sidebar.title("🔓 Logout")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.expenses = []
    st.rerun()

    
                

       

   
       
   

           

