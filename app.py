import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

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

# -------------------------
# LOGIN PAGE
# -------------------------
if not st.session_state.logged_in:
    st.title("🔐 Login to Expensify Lite")

    email = st.text_input("Email").strip()
    password = st.text_input("Password", type="password").strip()

    if st.button("Login"):
        if email and password:
            st.session_state.logged_in = True
            st.session_state.user = email
            st.success(f"✅ Welcome, {email}")
            st.experimental_rerun()
        else:
            st.warning("⚠️ Please enter both email and password")

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
    st.write("🧾 **Your Expenses**")
    st.dataframe(df, use_container_width=True)

    # Total Spend
    total = sum(e["Amount"] for e in filtered)
    st.metric("💰 Total Spent", f"₹{total:.2f}")

    # Category Chart
    cat_df = df.groupby("Category")["Amount"].sum().reset_index()
    st.subheader("📊 Spend by Category")
    st.bar_chart(cat_df, x="Category", y="Amount")

    # Download CSV
    csv = df.to_csv(index=False).encode()
    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name=f"{st.session_state.user}_expenses.csv",
        mime="text/csv"
    )
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
    st.experimental_rerun()

           

