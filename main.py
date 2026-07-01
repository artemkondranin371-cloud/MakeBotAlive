import telebot
from flask import Flask
from threading import Thread
import time

# ===== ТВОЙ ТЕЛЕГРАМ БОТ =====
TOKEN = "8862678941:AAHUGSVtp2qbCT3DSCMBqpvMsjb-JtX1EQY"
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🤖 Привет! Я работаю 24/7 благодаря UptimeRobot!")

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "Просто напиши мне что-нибудь, и я отвечу!")

# Обработчик любых текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, f"Ты сказал: {message.text}")

# ===== ВЕБ-СЕРВЕР ДЛЯ UPTIMEROBOT =====
app = Flask('')

@app.route('/')
def home():
    return "🤖 Бот жив и работает!"

def keep_alive():
    """Запускает веб-сервер в отдельном потоке"""
    def run():
        app.run(host='0.0.0.0', port=8080)
    t = Thread(target=run)
    t.start()

# ===== ЗАПУСК =====
if __name__ == "__main__":
    print("🚀 Запуск бота...")
    keep_alive()
    print("✅ Веб-сервер запущен, бот готов к работе!")
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
