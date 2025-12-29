import streamlit as st
import utils  # Your helper functions

st.set_page_config(page_title="MedCheck AI", page_icon="💊")

st.title("MedCheck AI")
st.write("Your MedCheck AI assistant for medicine checks and batch info.")

# Quick Medicine Check inputs
medicine_name = st.text_input("Medicine Name")
batch_number = st.text_input("Batch Number")
expiry_date = st.date_input("Expiry Date")

if st.button("Check Medicine"):
    if not medicine_name:
        st.warning("Please enter a medicine name")
    else:
        msg = f"Check medicine: {medicine_name}, Batch: {batch_number or 'N/A'}, Expiry: {expiry_date}"
        st.write(f"**You:** {msg}")
        # Get bot response
        reply = utils.get_bot_response(msg)
        st.success(f"**MedCheck AI:** {reply}")

# Chat section
st.subheader("Chat with MedCheck AI")
user_input = st.text_input("Ask me anything about medicines...")

if st.button("Send"):
    if user_input:
        st.write(f"**You:** {user_input}")
        reply = utils.get_bot_response(user_input)
        st.write(f"**MedCheck AI:** {reply}")
