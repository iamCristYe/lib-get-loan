import os
import flask
import telebot
from get_loan import get_loan


if os.path.exists("secret.py"):
    from secret import bot_token
else:
    bot_token = os.environ.get("telegram_bot_key")
TELEGRAM_BOT_KEY = bot_token
app = flask.Flask(__name__)
bot = telebot.TeleBot(TELEGRAM_BOT_KEY)

@app.route(f"/wake-up")
def wake():
    bot.remove_webhook()
    return "<html><script>window.close()</script></html>"

@app.route(f"/{TELEGRAM_BOT_KEY}")
def main():
    bot.send_message(
        -1001982849593,
        f"`{get_loan()}`[更新](https://active-loans-bot.azurewebsites.net/{TELEGRAM_BOT_KEY})",
        "MarkdownV2",
    )
    return "<html><script>window.close()</script></html>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
