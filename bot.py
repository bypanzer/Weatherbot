"""Weather bot"""


from pyowm import OWM
from pyowm.exceptions import api_response_error
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import simplejson


def start(update, _):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        "Hi There! \nI'm the Weather bot,Send me the name of any city and ill "
        "provide you with real time weather data of that place. As long as the "
        "place you entered is in the database\n send /help for more info"
    )


def help_cmd(update, _):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        'Possible inputs are:'
        '\n <code>city_name</code> : just send the name of the place as a message to me'
        '\n /info     : send this to know  more about me :)'
        '\n /help     : send this if you want me to send this message again'
        '\n /forecast <code>city_name</code>  : Gives you 5 day forecast of the given city  ',
        parse_mode="HTML"

    )


def info(update, _):
    """"Send the info of the bot"""
    update.message.reply_text(
        'I was created by : @nithin_joseph \n'
        'I was made using OpenWeatherMap API, Weatherbit API ,telegram-python-bot wrapper and @ceda_ei ;)'
    )


def weather_cmd(update, _):
    """"Get the weather"""
    # Openweathermap API call
    degree_sign = u'\N{DEGREE SIGN}'
    api_key = '33638dfd265a15bdc090bbb83039ac70'
    owm = OWM(api_key)
    try:
        observation = owm.weather_at_place(str(update.message.text))
        weather = observation.get_weather()
        temperature = weather.get_temperature(unit='celsius')['temp']
        humidity = weather.get_humidity()
        wind = weather.get_wind()['speed']
        wind = wind * 3.6
        pressure = weather.get_pressure()['press']
        cloud = weather.get_detailed_status()
        cloud_coverage = weather.get_clouds()
        update.message.reply_text(
            f"Following are the weather parameters at <b>{update.message.text.title()}</b>:"
            f"\n\n<b>Temprature</b>            <code>{temperature:.3}{degree_sign}C</code>"
            f"\n<b>Humidity</b>                 <code>{humidity}%</code>"
            f"\n<b>Wind speed</b>            <code>{wind:.4}km/h</code>"
            f"\n<b>Pressure</b>                 <code>{pressure}hPa</code>"
            f"\n<b>Weather</b>                   <code>{cloud}</code>"
            f"\n<b>Cloud coverage</b>     <code>{cloud_coverage}%</code>",
            parse_mode="HTML"
        )

    except api_response_error.NotFoundError:
        update.message.reply_text('Stop living in the middle of Nowhere')


def forecast(update, context):
    """Get the weather forecast for 5 days"""
    # Weatherbit API call
    degree_sign = u'\N{DEGREE SIGN}'
    city = str(context.args[0])
    url = 'https://api.weatherbit.io/v2.0/forecast/daily?city={}&key=445973c3b2c74d2196f0faf3d54faea7&days=5'.format(
        city)
    try:
        res = requests.get(url)
        full_data = res.json()['data']

        # classes defined
        cloud_coverage = []
        date = []
        wind_speed = []
        wind_direction = []
        average_temp = []
        minimum_temp = []
        maximum_temp = []
        feels_like = []
        chance_of_rain = []
        pressure = []
        humidity = []
        weather_description = []
        visibility = []
        max_uv_index = []

        # Date_attributed_to_classes

        for value in full_data:
            cloud = value['clouds']
            cloud_coverage.append(cloud)
            description = value['weather']['description']
            weather_description.append(description)
            valid_date = value['valid_date']
            date.append(valid_date)
            wind_spd = value['wind_spd']
            wind_speed.append(wind_spd)
            wind_cdir_full = value['wind_cdir_full']
            wind_direction.append(wind_cdir_full)
            temp = value['temp']
            average_temp.append(temp)
            min_temp = value['min_temp']
            minimum_temp.append(min_temp)
            max_temp = value['max_temp']
            maximum_temp.append(max_temp)
            app_max_temp = value['app_max_temp']
            feels_like.append(app_max_temp)
            pop = value['pop']
            chance_of_rain.append(pop)
            pres = value['pres']
            pressure.append(pres)
            rh = value['rh']
            humidity.append(rh)
            vis = value['vis']
            visibility.append(vis)
            uv = value['uv']
            max_uv_index.append(uv)

        r = 0
        while r < 5:
            update.message.reply_text("<b>Day</b> " + str(r + 1) +
                                      f"\n\n<b>Date</b>                                       <code>{date[r]}</code>"
                                      f"\n<b>Temp(min/max)</b>                 <code>{float(minimum_temp[r])}</code> / <code>{float(maximum_temp[r]):.3}{degree_sign}C</code>"
                                      f"\n<b>Average temperature</b>        <code>{float(average_temp[r]):.3}{degree_sign}C</code>"
                                      f"\n<b>But Feels like</b>                      <code>{float(feels_like[r]):.3}{degree_sign}C</code>"
                                      f"\n<b>Humiditiy</b>                             <code>{humidity[r]}%</code>"
                                      f"\n<b>Wind Speed</b>                         <code>{float(wind_speed[r])}m/s</code>"
                                      f"\n<b>Wind direction</b>                     <code>{wind_direction[r]}</code>"
                                      f"\n<b>Pressure</b>                               <code>{pressure[r]}mb</code>"
                                      f"\n<b>Visibility</b>                                <code>{visibility[r]}km</code>"
                                      f"\n<b>Uv Max Index</b>                       <code>{max_uv_index[r]}</code>"
                                      f"\n<b>Cloud coverage</b>                   <code>{cloud_coverage[r]}%</code>"
                                      f"\n<b>Weather</b>                                 <code>{weather_description[r]}</code>"
                                      f"\n<b>Chance of rain</b>                      <code>{chance_of_rain[r]}%</code>",
                                      parse_mode="HTML"
                                      )

            r = r + 1


    except simplejson.JSONDecodeError:
        update.message.reply_text('Forecast not available for this location')


def main():
    """Start the bot."""

    updater = Updater("1281818858:AAGg9htTeICPzd7t2CUn7X5lPoLsGbmLBQw", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_cmd))
    dispatcher.add_handler(CommandHandler("info", info))
    dispatcher.add_handler(CommandHandler("forecast", forecast))

    # on noncommand i.e message - weather of the given place
    dispatcher.add_handler(MessageHandler(Filters.text, weather_cmd))

    # Start the Bot
    updater.start_polling()

    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
