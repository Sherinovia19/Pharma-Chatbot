import streamlit as st
import utils
import datetime

st.set_page_config(page_title="MedCheck AI", layout="wide", page_icon="💊")

# Inject CSS for styling
st.markdown("""
<style>
body {
    font-family: 'Inter', sans-serif;
    background: #f1f5f9;
}
#chat-box {
    height: 400px;
    overflow-y: auto;
}
.chat-bubble {
    padding: 8px 12px;
    border-radius: 20px;
    max-width: 75%;
    margin-bottom: 8px;
}
.user { background-color: #3b82f6; color: white; align-self: flex-end; }
.bot { background-color: #bfdbfe; color: #1f2937; align-self: flex-start; }
.safe { background-color: #d1fae5; color: #065f46; }
.near_expiry { background-color: #fef3c7; color: #78350f; }
.expired { background-color: #fee2e2; color: #991b1b; }
.flex { display: flex; }
.flex-col { display: flex; flex-direction: column; }
.gap-2 { gap: 8px; }
</style>
""", unsafe_allow_html=True)

# Layout: two columns
left_col, right_col = st.columns([1,2])

with left_col:
    st.subheader("Quick Medicine Check")
    medicine_name = st.text_input("Medicine Name *", "")
    batch_number = st.text_input("Batch Number", "")
    expiry_date = st.date_input("Expiry Date", datetime.date.today())
    if st.button("Check Medicine"):
        if not medicine_name:
            st.warning("Please enter medicine name")
        else:
            msg = f"Check medicine: {medicine_name}, Batch: {batch_number or 'N/A'}, Expiry: {expiry_date}"
            st.session_state.chat.append({"sender":"user", "text": msg})
            reply = utils.get_bot_response(msg)
            st.session_state.chat.append({"sender":"bot", "text": reply, "type":"normal"})

with right_col:
    st.subheader("Chat with MedCheck AI")

    # Initialize chat history
    if "chat" not in st.session_state:
        st.session_state.chat = []

    # Display chat messages
    for msg in st.session_state.chat:
        cls = "user" if msg["sender"]=="user" else "bot"
        if msg.get("type"): cls = msg["type"]
        st.markdown(f'<div class="chat-bubble {cls}">{msg["text"]}</div>', unsafe_allow_html=True)

    # Input box
    user_input = st.text_input("Type a message...", "")
    if st.button("Send Message"):
        if user_input:
            st.session_state.chat.append({"sender":"user","text":user_input})
            reply = utils.get_bot_response(user_input)
            # classify response
            type_ = "normal"
            r = reply.lower()
            if "expired" in r or "recalled" in r: type_="expired"
            elif "near expiry" in r: type_="near_expiry"
            elif "ok" in r: type_="safe"
            st.session_state.chat.append({"sender":"bot","text":reply,"type":type_})
