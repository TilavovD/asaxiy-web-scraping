import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from bs4 import BeautifulSoup
import requests


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        f'Hi {user.mention_markdown_v2()}'
    )


def send(update: Update, context: CallbackContext):
    url = "https://asaxiy.uz/product?key=telefon"
    response = requests.get(url)
    file = response.content
    soup = BeautifulSoup(file, "html.parser")
    products = soup.find_all("div", class_="product__item d-flex flex-column justify-content-between")[:10]

    for product in products:
        img = product.find("div", class_="product__item-img").img["data-src"]
        product_title = product.find("h5").text.strip()
        old_price = product.find("span", class_="product__item-old--price")
        old_price_text = ""
        if old_price:
            old_price_text = old_price.text
        price = product.find("span", class_="product__item-price").text.strip()
        payment_detail = product.find("div", class_="installment__price").text.strip()
        text = ""
        text += f"<a href='{img}'>{product_title}</a>\n\nNarxi: <strike>{old_price_text}</strike>\n{price}\n\n{payment_detail}"

        update.message.reply_text(text, parse_mode="HTML")




def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("Token")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("send", send))


    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
