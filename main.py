import json
import os
import telebot
from telebot import types

TOKEN = "8012810623:AAEaV5t2sWe9HS5UxluACsUzRSLZrxrhyKM"  # Asegúrate de poner tu token aquí
USERS_FILE = "users.json"
WEBAPP_URL = "https://github.com/gree22/bot-whytly-1.git
"  # URL de la WebApp

bot = telebot.TeleBot(TOKEN)

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    referral_id = message.text.split()[1] if len(message.text.split()) > 1 else None  # Obtener el ID de referido si existe

    # Generar enlace de referido para la WebApp
    webapp_url = f"{WEBAPP_URL}?referral={user_id}"

    # Cargar los usuarios existentes
    users = load_users()

    if user_id not in users:
        # Si el usuario no está registrado, pedimos el ID de Payeer
        users[user_id] = {
            "telegram_id": user_id,
            "referido_por": referral_id,  # Almacenar el ID del usuario que lo refirió
            "payeer_id": None,  # El ID de Payeer será solicitado después
        }
        save_users(users)

        # Pedir el ID de Payeer
        bot.reply_to(message, "Por favor, envíame tu ID de Payeer para completar el registro.")
    else:
        # Crear el botón con InlineKeyboardMarkup para abrir la WebApp dentro de Telegram
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Earn money", web_app=types.WebAppInfo(webapp_url))
        markup.add(button)

        # Enviar el mensaje con el botón
        bot.send_message(
            message.chat.id,
            "👋 ¡Bienvenido de nuevo! Usa el botón para ir a la WebApp y comenzar a trabajar:",
            reply_markup=markup
        )

@bot.message_handler(func=lambda message: True)
def recibir_payeer_id(message):
    user_id = str(message.from_user.id)
    users = load_users()

    if user_id in users and users[user_id]["payeer_id"] is None:
        # Guardamos el ID de Payeer
        users[user_id]["payeer_id"] = message.text.strip()
        save_users(users)

        # Generar el enlace de la WebApp
        webapp_url = f"{WEBAPP_URL}?referral={user_id}"

        # Crear el botón con InlineKeyboardMarkup para abrir la WebApp dentro de Telegram
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Earn money", web_app=types.WebAppInfo(webapp_url))
        markup.add(button)

        # Enviar el mensaje con el botón
        bot.send_message(
            message.chat.id,
            "🎉 ¡Te has registrado exitosamente! Ahora puedes comenzar a trabajar en la WebApp.",
            reply_markup=markup
        )
    else:
        bot.reply_to(message, "❌ No es necesario que ingreses el ID de Payeer ahora.")

if __name__ == '__main__':
    bot.infinity_polling()
