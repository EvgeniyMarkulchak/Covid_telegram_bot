import requests
import json

import telebot

import config
import bot_data


bot = telebot.TeleBot(config.token)
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Russia', 'Ukraine', 'USA', 'Italy', 'Spain', 'China', 'France', 'Germany', 'UK')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        'Привет! Давай посмотрим как дела с пандемией. Нажми на кнопку или напиши страну сам (обязательно на английском).',
        reply_markup=keyboard1
        )

@bot.message_handler(content_types=["text"])
def send_text(message):
    country = message.text.lower()
    country_boolean = country in bot_data.lower_countries
    if country_boolean:
        url = "https://covid-193.p.rapidapi.com/statistics"
        querystring = {"country":f"{country}"}
        headers = {
            'x-rapidapi-host': "covid-193.p.rapidapi.com",
            'x-rapidapi-key': config.x_rapidapi_key
        }
        response = requests.request("GET", url, headers=headers, params=querystring)

        covid19_answer = response.text
        json_answer = json.loads(covid19_answer)
        sick_data = json_answer['response']

        new_sick = sick_data[0]['cases']['new']
        active_sick = sick_data[0]['cases']['active']
        critical_sick = sick_data[0]['cases']['critical']
        recovered_sick = sick_data[0]['cases']['recovered']
        total_sick = sick_data[0]['cases']['total']
        new_deaths = sick_data[0]['deaths']['new']
        total_deaths = sick_data[0]['deaths']['total']

        print('Пользователь получает данные.')
        
        bot.send_message(message.chat.id, (f"Данные по {country.capitalize()} таковы... \n 🚑 Новых заболевших: {new_sick} \n" 
        f" ☣️ Заболевших сейчас: {active_sick} \n 💉 В тяжелом состоянии: {critical_sick} \n ✨ Выздоровели: {recovered_sick} \n 🏨 Заболевших"
        f" за всё время: {total_sick} \n 💔 Умерло: {new_deaths} \n 🖤 Всего умерло: {total_deaths}"))
    else:
        bot.send_message(message.chat.id, ("Неправильное название страны на английском или отсутсвуют данные!"
        " Названия стран в два и более слова пишутся так: Bosnia-and-Herzegovina"))        

bot.polling()

