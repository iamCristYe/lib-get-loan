import os
import flask
import telebot
from datetime import datetime
from main import main

TELEGRAM_BOT_KEY = os.environ.get("telegram_bot_key")
app = flask.Flask(__name__)
bot = telebot.TeleBot(TELEGRAM_BOT_KEY)


# non-command message
@bot.message_handler(func=lambda m: True)
# start command
@bot.message_handler(commands=["start"])
def handle_message_and_command(message):
    bot.send_message(-1001982849593, main())  # Channel


# We use telegram_bot_key as the web hook route
@app.route(f"/{TELEGRAM_BOT_KEY}", methods=["POST"])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(flask.request.stream.read().decode("utf-8"))]
    )
    return "<HTML><HEAD><TITLE>Success</TITLE></HEAD><BODY>Success</BODY></HTML>"


@app.route("/")
def index():
    bot.remove_webhook()
    bot.set_webhook(
        url=f"https://active-loans-bot.azurewebsites.net/{TELEGRAM_BOT_KEY}"
    )
    bot.send_message(-1001982849593, main())  # Channel
    return "<HTML><HEAD><TITLE>Success</TITLE></HEAD><BODY>Success</BODY></HTML>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
