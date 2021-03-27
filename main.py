import os
import logging
import requests

from urllib.parse import urljoin

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

PORT = int(os.environ.get("PORT", 5000))
TOKEN = os.environ["TOKEN"]
NAME = os.environ["NAME"]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger()


def get_meme_url(subreddit: str = None):
    url = "https://meme-api.herokuapp.com/gimme"
    if subreddit:
        url = urljoin(url + "/", subreddit)

    logger.info("Url %s" % url)
    r = requests.get(url).json()
    logger.info("Got json response: %s" % r)
    return r["url"]


def error_handler(update: Update, context: CallbackContext):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text="Sounds good, does not work... :(")


def send_meme(update: Update, context: CallbackContext):
    logger.info("Got update: %s" % update)
    logger.info("Got args: %s" % context.args)
    url = get_meme_url(*context.args)
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    # noinspection PyTypeChecker
    dp.add_error_handler(error_handler)
    dp.add_handler(CommandHandler("meme", send_meme, pass_args=True))

    logging.info(f"Start webhook mode on port {PORT}")
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()


if __name__ == "__main__":
    main()
