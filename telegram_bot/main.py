import configparser
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import start_crawler

# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

#Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

bot = token=(config['TELEGRAM']['ACCESS_TOKEN'])

def hello(update: Update, context: CallbackContext):
    update.message.reply_text(
        'hello, {}'.format(update.message.from_user.first_name))

def update_all(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Hello, {}'.format(update.message.from_user.first_name))

    update.message.reply_text(
        'We will now update all data to database')
    ####

def update_course(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Hello, {}'.format(update.message.from_user.first_name))

    update.message.reply_text(
        'We will now update course data to database\n...\n..\n.')

    start_crawler.crawl_Course()


    update.message.reply_text(
        'Finish update')



updater = Updater(bot, use_context=True)

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('update_all', update_all))
updater.dispatcher.add_handler(CommandHandler('update_course', update_course))

updater.start_polling()
updater.idle()
