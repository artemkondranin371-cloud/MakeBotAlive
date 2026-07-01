print("Бот запускается...")
import telebot
from flask import Flask
from threading import Thread
import time

TOKEN = "8862678941:AAHUGSVtp2qbCT3DSCMBqpvMsjb-JtX1EQY"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я на Render!")

app = Flask('')

@app.route('/')
def home():
    return "Бот жив!"

def keep_alive():
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

if __name__ == "__main__":
    keep_alive()
    print("Бот запущен, жду сообщения...")
    bot.polling()
