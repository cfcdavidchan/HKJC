import configparser
import logging
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import start_crawler
import subprocess

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
        'We will now update all data to database\n...\n..\n.')

    start_crawler.crawl_Course()
    update.message.reply_text(
        'Finish update Course')

    start_crawler.crawl_Trainer()
    update.message.reply_text(
        'Finish update Trainer')

    start_crawler.crawl_Jockeys()
    update.message.reply_text(
        'Finish update Jokceys')

    start_crawler.crawl_Hourse()
    update.message.reply_text(
        'Finish update Hourse')

    start_crawler.crawl_Match()
    update.message.reply_text(
        'Finish update Match')

    update.message.reply_text(
        'Finish update')



def update_recentmatch(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Hello, {}'.format(update.message.from_user.first_name))

    update.message.reply_text(
        'We will now update the recent match data\n...\n..\n.')

    start_crawler.crawl_RecentMatch()
    update.message.reply_text(
        'Finish update RecentMatch')

    update.message.reply_text(
        'Now sending data to Google')
    path = os.getcwd()
    project_path = os.path.dirname(path)
    google_spreadsheet_path = os.path.join(project_path, 'google_spreadsheet')
    commnad = 'python update_spreadsheet.py'
    subprocess.Popen(commnad, shell=True, cwd=google_spreadsheet_path, executable="/bin/bash").wait()

    update.message.reply_text(
        'Finish sending data to Google')



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
updater.dispatcher.add_handler(CommandHandler('update_recentmatch', update_recentmatch))

updater.start_polling()
updater.idle()
