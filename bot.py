from pyowm import OWM
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pyowm.exceptions import api_response_error


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hi There! \nI'm the Weather bot,Send me the name of any city and ill provide you with "
                              "real time weather data of that place. As long as the place you entered is in the "
                              "database"
                              "\n send /help for more info")


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Possible inputs are:'
                              '\n city_name : just send the name of the place as a message to me'
                              '\n /info     : send this to know  more about me :)'
                              '\n /help     : send this if you want me to send this message again'
                              '\n more feature will be added soon  ')


def info(update, context):
    """"Send the info of the bot"""
    update.message.reply_text(
        'I was created by : @nithin_joseph \nI was made using OpenWeatherMap API and telegram-python-bot wrapper')


def weather(update, context):
    """"Get the weather"""
    # Openweathermap API call
    degree_sign = u'\N{DEGREE SIGN}'
    API_key = '33638dfd265a15bdc090bbb83039ac70'
    owm = OWM(API_key)
    try:
        observation = owm.weather_at_place(str(update.message.text))
        weather = observation.get_weather()
        temperature = weather.get_temperature(unit='celsius')['temp']
        humidity = weather.get_humidity()
        wind = weather.get_wind()['speed']
        wind = wind * 3.6
        wind = round(wind, 3)
        pressure = weather.get_pressure()['press']
        cloud = weather.get_detailed_status()
        cloud_coverage = weather.get_clouds()
        update.message.reply_text("Following are the weather parameters at " + str(update.message.text).upper()  + ":"
                                  "\nTemprature         = "+ str(temperature) + degree_sign + 'C'
                                  "\nHumidity              = " + str(humidity) + "%"
                                  "\nWind speed         = " + str(wind) + "km/h"
                                  "\nPressure               = " + str(pressure) + "hPa"
                                  "\nWeather                = " + str(cloud)  +""
                                  "\nCloud coverage  = " + str(cloud_coverage) + "%"
                                  )

    except api_response_error.NotFoundError:
        update.message.reply_text('Stop living in the middle of Nowhere')


def main():
    """Start the bot."""

    updater = Updater("1281818858:AAGg9htTeICPzd7t2CUn7X5lPoLsGbmLBQw", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("info", info))

    # on noncommand i.e message - weather of the given place
    dp.add_handler(MessageHandler(Filters.text, weather))

    # Start the Bot
    updater.start_polling()

    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
