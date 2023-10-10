import os
import flask
import telebot
from get_loan import get_loan

TELEGRAM_BOT_KEY = os.environ.get("telegram_bot_key")
app = flask.Flask(__name__)
bot = telebot.TeleBot(TELEGRAM_BOT_KEY)


@app.route(f"/{TELEGRAM_BOT_KEY}")
def main():
    bot.remove_webhook()
    bot.send_message(
        -1001982849593,
        f"`{get_loan()}`\n[refresh](https://active-loans-bot.azurewebsites.net/{TELEGRAM_BOT_KEY})",
        telebot.formatting.escape_markdown,
    )
    return "<html><script>window.close()</script></html>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
