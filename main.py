import configparser
import logging
import json
from lib.FoodData import FOOD_DATABASE
from flask import Flask, request
import telegram
from telegram import ReplyKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters



# Load data from config.ini and version.ini file
config = configparser.ConfigParser()
config.read('config.ini')
version = configparser.ConfigParser()
version.read('version.ini')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initial Flask app
app = Flask(__name__)

# Initial bot by Telegram access token
bot = telegram.Bot(token=(TELEGRAM_BOT_TOKEN))

#Initial food_database 
food_database = FOOD_DATABASE()

welcome_message = '此推薦系統版本為' + version['VERSION']['CODE_VERSION'] + '\n' \
                  '此資料庫版本為' + version['VERSION']['DATABSE_VERSION'] + '\n' \
                  '您可以選擇你想要的類別\n' \
                  '或是選擇一日一推薦'
reply_keyboard_markup = ReplyKeyboardMarkup(food_database.get_main_category())

@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return 'ok'


def start_handler(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text(welcome_message, reply_markup=reply_keyboard_markup)


def help_handler(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text(welcome_message, reply_markup=reply_keyboard_markup)


def reply_handler(bot, update):
    """Reply message."""
    text = update.message.text
    user_id = update.message.from_user.id
    bot.sendChatAction(user_id, 'typing')
    if text == '回到主選單':
        update.message.reply_text(welcome_message, reply_markup=reply_keyboard_markup)
    elif food_database.have_this_category(text) == True :
        update.message.reply_text('請選擇餐廳',reply_markup=ReplyKeyboardMarkup(food_database.get_category_restaurant(text)))
    elif food_database.have_this_restaurant(text) == True :
        temp = food_database.get_this_restaurant(text)
        update.message.reply_text(
            '餐廳名：' + temp['name'] + '\n' \
            '餐廳地址：' + temp['address'] + '\n' \
            '餐廳電話：' + temp['phone'] + '\n' \
            '餐廳營業時間：' + temp['time'] + '\n' \
            '餐廳介紹：' + temp['description'] + '\n' \
            'google map：' + 'https://www.google.com/maps/search/?api=1&query=' +temp['address']
        )
    elif text[:5] == '一日一推薦' :
        if len(text) == 5 :
            temp = food_database.get_rand_restaurant()
        elif food_database.have_this_category(text[6:]) == True :
            temp = food_database.get_rand_restaurant(category = text[6:])
        else :
            update.message.reply_text('對不起，我不了解！',reply_markup=reply_keyboard_markup)
            return
        update.message.reply_text(
            '餐廳名：' + temp['name'] + '\n' \
            '餐廳地址：' + temp['address'] + '\n' \
            '餐廳電話：' + temp['phone'] + '\n' \
            '餐廳營業時間：' + temp['time'] + '\n' \
            '餐廳介紹：' + temp['description'] + '\n' \
            'google map：' + 'https://www.google.com/maps/search/?api=1&query=' +temp['address']
        )
    else :
        update.message.reply_text('對不起，我不了解！',reply_markup=reply_keyboard_markup)


def error_handler(bot, update, error):
    """Log Errors caused by Updates."""
    logger.error('Update "%s" caused error "%s"', update, error)
    update.message.reply_text('對不起主人，我需要多一點時間來處理 Q_Q')

# New a dispatcher for bot
dispatcher = Dispatcher(bot, None)

# Add handler for handling message, there are many kinds of message.
# For this handler, it particular handle text message.
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))
dispatcher.add_handler(CommandHandler('start', start_handler))
dispatcher.add_handler(CommandHandler('help', help_handler))
dispatcher.add_error_handler(error_handler)

if __name__ == "__main__":
    # Running server
    app.run(debug=True)