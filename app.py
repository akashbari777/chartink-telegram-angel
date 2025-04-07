@app.route("/webhook", methods=["POST"])
def telegram_callback():
    data = request.json

    # Check if it's a button click (callback query)
    if "callback_query" in data:
        query = data["callback_query"]
        action, stock = query["data"].split(":")
        callback_id = query["id"]

        # Acknowledge the button press
        bot.answer_callback_query(callback_query_id=callback_id)

        # Respond to user
        bot.send_message(chat_id=CHAT_ID, text=f"{action} clicked for {stock}")
        return "Callback processed", 200

    return "Not a callback", 200
