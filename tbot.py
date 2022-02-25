#!pip install python-telegram-bot --upgrade
`
import random
import nltk
import json

#BOT_CONFIG = {
#    'intents': {
#        'hello': {
#          'examples': ['Привет!', 'хэллоу', 'добрый день!!'],
#          'responses': ['хай', 'Здравствуйте', 'Доброе утро!']
#        },
#        'bye': {
#          'examples': ['Пока!', 'увидимся', 'счастливо'],
#          'responses': ['до свиданья', 'до скорых встреч', 'Спокойной ночи)']
#        }
#    }
#}

with open('BOT_CONFIG.json', 'r') as f:
  BOT_CONFIG = json.load(f)

def clean(text):
  clean_text = ''
  for char in text. lower():
    if char in 'абвгдеёжзийклмнопрстуфхцчшщьыьэюяabcdefghijklmnoqrstuvwxyz':
      clean_text = clean_text + char
  return clean_text

def get_intent(text):
  for intent in BOT_CONFIG['intents'].keys():
    for example in BOT_CONFIG['intents'] [intent] ['examples']:
      s1 = clean(text)
      s2 = clean(example)
      if nltk.edit_distance(s1, s2) / max(len(s1), len(s2)) < 0.4:
          return intent   
  return 'intent not found :('

def bot(text):
  intent = get_intent(text)
  if intent != 'intent not found :(':
    return(random.choice(BOT_CONFIG['intents'] [intent] ['responses']))
  else:
    return('я не понял, попробуйте сформулировать по-другому')



#input_text = ''
#while input_text != 'STOP':
#  input_text = input()
#  bot(input_text)



from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext



# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user  = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    input_text = update.message.text
    reply = bot(input_text)
    update.message.reply_text(reply)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5029814489:AAH6gCRY6pjAHoTREsrGyCcs4tR7-K7QSik")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Запускаем цикл приема и обработки сообщений
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()