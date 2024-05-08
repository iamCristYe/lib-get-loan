import os
import flask
import telebot
from get_loan import get_loan, get_loan_nblib_str
import hashlib


if os.path.exists("secret.py"):
    from secret import bot_token
else:
    bot_token = os.environ.get("telegram_bot_key")
TELEGRAM_BOT_KEY = bot_token
bot_token_md5 = hashlib.md5(bot_token.encode()).hexdigest()

app = flask.Flask(__name__)
bot = telebot.TeleBot(TELEGRAM_BOT_KEY)


@app.route(f"/{bot_token_md5}")
def main():
    bot.send_message(
        -1001982849593,
        f"`{get_loan_nblib_str()}`[更新](https://active-loans-bot.azurewebsites.net/{bot_token_md5})",
        "MarkdownV2",
        disable_web_page_preview=True,
    )
    bot.send_message(
        -1001982849593,
        f"`{get_loan()}`[更新](https://active-loans-bot.azurewebsites.net/{bot_token_md5})",
        "MarkdownV2",
        disable_web_page_preview=True,
    )
    return "<html><script>window.close()</script></html>"


@app.route("/<path:path>")
def catch_all(path):
    bot.remove_webhook()
    return "<html><script>window.close()</script></html>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
