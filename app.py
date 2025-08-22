import streamlit as st
from hello import Bank

bank = Bank()

st.title("🏦 Simple Bank System")

menu = ["Create Account", "Deposit", "Withdraw", "Show Details", "Update Details", "Delete Account"]
choice = st.sidebar.selectbox("Menu", menu)


# ---------- Helper for displaying messages ----------
def display_result(ok, msg):
    if ok:
        if isinstance(msg, dict):
            st.json(msg)
        else:
            st.success(msg)
    else:
        st.error(msg)


# ---------- Menu Actions ----------
if choice == "Create Account":
    st.subheader("Create a New Account")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, step=1)
    email = st.text_input("Email")
    pin = st.text_input("4-digit PIN", type="password")
    if st.button("Create"):
        if not pin.isdigit():
            st.error("PIN must be numeric")
        else:
            ok, msg = bank.create_account(name, int(age), email, int(pin))
            display_result(ok, msg)

elif choice == "Deposit":
    st.subheader("Deposit Money")
    acc = st.text_input("Account Number").strip()
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)
    if st.button("Deposit"):
        ok, msg = bank.deposit(acc, pin, amount)
        display_result(ok, msg)

elif choice == "Withdraw":
    st.subheader("Withdraw Money")
    acc = st.text_input("Account Number").strip()
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)
    if st.button("Withdraw"):
        ok, msg = bank.withdraw(acc, pin, amount)
        display_result(ok, msg)

elif choice == "Show Details":
    st.subheader("Account Details")
    acc = st.text_input("Account Number").strip()
    pin = st.text_input("PIN", type="password")
    if st.button("Show"):
        ok, msg = bank.show_details(acc, pin)
        display_result(ok, msg)

elif choice == "Update Details":
    st.subheader("Update Account Details")
    acc = st.text_input("Account Number").strip()
    pin = st.text_input("PIN", type="password")
    name = st.text_input("New Name (leave blank if no change)")
    email = st.text_input("New Email (leave blank if no change)")
    new_pin = st.text_input("New 4-digit PIN (leave blank if no change)", type="password")

    if st.button("Update"):
        new_pin_val = int(new_pin) if new_pin.isdigit() else None
        ok, msg = bank.update_details(acc, pin, name or None, email or None, new_pin_val)
        display_result(ok, msg)

elif choice == "Delete Account":
    st.subheader("Delete Account")
    acc = st.text_input("Account Number").strip()
    pin = st.text_input("PIN", type="password")
    if st.button("Delete"):
        ok, msg = bank.delete_account(acc, pin)
        display_result(ok, msg)
