from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import re
import random

app = Flask(__name__)

faq_responses = {
    "hello": "Welcome to PaulTechTelecom! Ask me anything like 'Buy MTN data' or 'Fund wallet'.",
    "buy data": "Sure! What network? We have MTN, Glo, Airtel, and 9mobile. Reply with the one you want.",
    "fund wallet": "To fund your wallet, transfer to the account shown on your dashboard at paultechtelecom.com.ng. It will auto-fund.",
    "pricing": "You can view the latest pricing for data and airtime at https://paultechtelecom.com.ng/pricing",
    "mtn": "MTN Data Plans:\n500MB = N130\n1GB = N250\n2GB = N480\nReply with amount to proceed.",
    "glo": "Glo Data Plans:\n500MB = N140\n1GB = N270\n2GB = N500\nReply with amount to proceed.",
    "airtel": "Airtel Data Plans:\n500MB = N135\n1GB = N260\n2GB = N490\nReply with amount to proceed.",
    "9mobile": "9mobile Data Plans:\n500MB = N150\n1GB = N280\n2GB = N510\nReply with amount to proceed."
}

def get_wallet_balance(phone_number):
    return f"Your wallet balance is N{random.randint(100, 5000)}."

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()

    phone_match = re.search(r"\b(\d{10,13})\b", incoming_msg)
    if phone_match:
        phone = phone_match.group(1)
        balance = get_wallet_balance(phone)
        msg.body(f"Phone number detected: {phone}\n{balance}")
        return str(resp)

    response = "I'm sorry, I didn't understand that. You can say things like 'Buy MTN data', 'Fund wallet', or send your phone number to check your wallet balance."

    for key in faq_responses:
        if key in incoming_msg:
            response = faq_responses[key]
            break

    msg.body(response)
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
