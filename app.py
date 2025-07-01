import streamlit as st

st.set_page_config(page_title="Expensify Lite 💸", layout="centered")

st.title("💸 Expensify Lite")
st.write("Welcome to your smart expense tracker app, Zaina! 🚀")

expense = st.text_input("Enter your expense note:")
amount = st.number_input("Enter amount", min_value=0.0, format="%.2f")

if st.button("Submit"):
    st.success(f"Saved: {expense} - ₹{amount}")
