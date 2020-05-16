from pyowm import OWM
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hi There! \nI'm the demo weather bot, just send me the name of a city and i'll provide you with the curent temperature there" )


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Just message me the name of a city ')


def weather(update, context):
    """"Get the weather"""
    # Openweathermap API call
    degree_sign = u'\N{DEGREE SIGN}'
    API_key = '33638dfd265a15bdc090bbb83039ac70'
    owm = OWM(API_key)
    observation = owm.weather_at_place(str(update.message.text))
    weather = observation.get_weather()
    temperature = weather.get_temperature(unit='celsius')['temp']

    # API Call End
    update.message.reply_text("The temperature at " + str(update.message.text) + ' is ' + str(temperature) + degree_sign + 'C')


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1281818858:AAGg9htTeICPzd7t2CUn7X5lPoLsGbmLBQw", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - weather of the given place
    dp.add_handler(MessageHandler(Filters.text, weather))


    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
