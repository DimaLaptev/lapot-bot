from telegram.ext import CommandHandler, Updater, Filters, MessageHandler
from telegram import ReplyKeyboardMarkup
import requests
import os


auth_token = os.getenv('TOKEN')
updater = Updater(token=auth_token)
URL = 'https://api.thecatapi.com/v1/images/search'

def get_new_image():
    try:
        response = requests.get(URL).json()
    except Exception as error:
        print(error)      
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
    random_cat = response[0].get('url')
    return random_cat

def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())

def wake_up(update, context):
    # В ответ на команду /start 
    # будет отправлено сообщение 'Спасибо, что включили меня'
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/newcat']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Кожаный товарищ {}! Посмотри, какого котика я тебе нашёл'.format(name),
        reply_markup=button,
    )
    context.bot.send_photo(chat.id, get_new_image())

updater.dispatcher.add_handler(CommandHandler('start', wake_up))

updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))

updater.start_polling()

updater.idle()
