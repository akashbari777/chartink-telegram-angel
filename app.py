from flask import Flask, request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

@app.route("/chartink", methods=["POST"])
def chartink_webhook():
    data = request.json
    stock = data.get("stock", "UNKNOWN")
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("BUY", callback_data=f"BUY:{stock}"),
         InlineKeyboardButton("SELL", callback_data=f"SELL:{stock}")]
    ])
    bot.send_message(chat_id=CHAT_ID, text=f"Chartink Alert: {stock}", reply_markup=keyboard)
    return "Alert sent"

@app.route("/webhook", methods=["POST"])
def telegram_callback():
    data = request.json
    query = data['callback_query']
    action, stock = query['data'].split(":")
    bot.answer_callback_query(query['id'])
    bot.send_message(chat_id=CHAT_ID, text=f"{action} clicked for {stock}")
    return "Action received"
