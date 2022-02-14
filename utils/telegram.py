import json, functools, datetime

import utils as u
from utils import binance as ub

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

###############################################################################
# Wrappers
###############################################################################
def check_id(func):
    '''Check if id is aloud to communicate with bot'''
    @functools.wraps(func)
    def wrap(update: Update, context: CallbackContext):
        user = update.effective_user
        if user.id not in u.get_const('valid_id'):
            update.message.reply_text('You are not authorized')
            u.log.info(f'User {user.id} ({user.full_name}) tried to connect')
            return
        else:
            func(update, context)
    return wrap

def failsafe(func):
    '''Manage errors'''
    @functools.wraps(func)
    def wrap(update: Update, context: CallbackContext):
        try: func(update, context)
        except:
            update.message.reply_text('Something went wrong')
    return wrap

###############################################################################
# Responses
###############################################################################
@check_id
def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    user = update.effective_user
    update.message.reply_text('Let s start this shit')
    u.flog.info(f'{user.id} - {user.full_name} tried to connect')

@check_id
def help_command(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('I cannot do much yet, sorry')

@check_id
@failsafe
def portfolio(update: Update, context: CallbackContext):
    """Send a message when the command /pf is issued."""
    bal = ub.get_balance()
    for i in u.pretty_df(bal):
        update.message.reply_text(i)

###############################################################################
@check_id
@failsafe
def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    u.log.info(f'{update.effective_user.id} - {update.message.text}')
    update.message.reply_text(eval(update.message.text))


###############################################################################
# Spontaneous
###############################################################################
def monitor(context: CallbackContext):
    message = u.get_const('message')
    if not message: return
    u.set_const({'message': ''})
    # send message to all users
    for id in u.get_const('valid_id'):
        u.log.info(f'Sending {message} to {id}')
        context.bot.send_message(chat_id=id, text=message)

def pf_update(context: CallbackContext):
    # send message to all users
    for id in u.get_const('valid_id'):
        u.log.info(f'Sending update to {id}')
        bal = ub.get_balance()
        for i in u.pretty_df(bal):
            context.bot.send_message(chat_id=id, text=i)

###############################################################################
def main(token):
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    job = updater.job_queue

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("pf", portfolio))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    job.run_repeating(monitor, 1)
    job.run_daily(pf_update, datetime.time(17, 9, 0))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
