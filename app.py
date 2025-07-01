import streamlit as st

st.title("💸 Smart Expense Tracker")
st.markdown("Track your daily expenses easily. Add amount and category, and get a quick summary!")

amount = st.number_input("Enter amount (₹):", min_value=0.0, format="%.2f")
category = st.text_input("Enter category (e.g. Food, Travel, Books)")

if 'expenses' not in st.session_state:
    st.session_state.expenses = []

if st.button("➕ Add Expense"):
    if amount and category:
        st.session_state.expenses.append((amount, category))
        st.success(f"Added ₹{amount:.2f} for {category}")
    else:
        st.warning("Please enter both amount and category")

if st.session_state.expenses:
    st.subheader("📋 Expense Summary")
    total = 0
    for amt, cat in st.session_state.expenses:
        st.write(f"💸 ₹{amt:.2f} — {cat}")
        total += amt

    st.markdown(f"**✅ Total Spent: ₹{total:.2f}**")

