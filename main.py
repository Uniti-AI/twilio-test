import os

import streamlit as st
from twilio.rest import Client

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv('.env'))

# Twilio credentials (replace with your own)
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
from_twilio_number = os.getenv('FROM_TWILIO_NUMBER')
to_twilio_number = os.getenv('TO_TWILIO_NUMBER')

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Function to send an SMS
def send_sms(message_body):
    message = client.messages.create(
        body=message_body,
        from_=from_twilio_number,
        to=to_twilio_number
    )
    return message.sid

# Streamlit App UI
st.title("Twilio SMS App")
st.markdown(f'From Number: {from_twilio_number} (Lead)')
st.markdown(f'To Number: {to_twilio_number} (Aron)')


# Input for phone number and message
message_body = st.text_area("Message")


if st.button("Send SMS"):
    if message_body:
        try:
            message_sid = send_sms(message_body)
            st.success(f"SMS sent! SID: {message_sid}")
        except Exception as e:
            st.error(f"Failed to send SMS: {e}")
    else:
        st.error("Please provide both a phone number and message.")


colum_1, column_2 = st.columns(2, gap='medium')
with colum_1:
    if st.button(f"List Received SMS: {from_twilio_number} (Lead)"):
        try:
            received_messages = client.messages.list(to=from_twilio_number, page_size=20)
            if received_messages:
                for message in received_messages:
                    st.markdown('__' * 100)
                    st.write(f"Received at: {message.date_sent} \n")
                    st.write(f"Message: {message.body}, \n")
                    st.write(f"From: {message.from_}\n\n")
            else:
                st.write("No messages received.")
        except Exception as e:
            st.error(f"Failed to fetch received messages: {e}")

with column_2:
    if st.button(f"List Received SMS : {to_twilio_number} (Aron)"):
        try:
            received_messages = client.messages.list(to=to_twilio_number, page_size=20)
            if received_messages:
                for message in received_messages:
                    st.markdown('__' * 100)
                    st.write(f"Received at: {message.date_sent} \n")
                    st.write(f"Message: {message.body}, \n")
                    st.write(f"From: {message.from_}\n\n")
            else:
                st.write("No messages received.")
        except Exception as e:
            st.error(f"Failed to fetch received messages: {e}")