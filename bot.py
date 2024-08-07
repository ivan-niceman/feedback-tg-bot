import telebot
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))

user_states = {}
user_name = ""
user_lastname = ""
min_review_length = 100
chat_id = 437153054

@bot.message_handler(commands=['start'])
def start(message):
  global user_name, user_lastname
  # Check if the user has a state
  user_states[message.chat.id] = "waiting_name"  # Set initial state

  # Send a welcome message
  bot.send_message(message.chat.id, "Добрый день!")

  # Ask the first question
  bot.send_message(message.chat.id, "Как вас зовут?")

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
  global user_name, user_lastname
  if user_states.get(message.chat.id) == "waiting_name":
    user_states[message.chat.id] = "waiting_lastname"
    user_name = message.text
    bot.send_message(message.chat.id, f"Спасибо, {user_name}! Теперь укажите вашу фамилию.")
  elif user_states.get(message.chat.id) == "waiting_lastname":
    user_states[message.chat.id] = "waiting_review"
    user_lastname = message.text
    bot.send_message(message.chat.id, f"Отлично, {user_name} {user_lastname}! Пожалуйста, оставьте отзыв о том, как прошла ваша смена в лагере Embassy Camps")
  elif user_states.get(message.chat.id) == "waiting_review":
    if len(message.text) < min_review_length:
      bot.send_message(message.chat.id, f"Ваш отзыв слишком короткий. Пожалуйста, напишите отзыв длиной не менее {min_review_length} символов.")
    else:
      review = message.text
      bot.send_message(message.chat.id, f"Спасибо за ваш отзыв, {user_name} {user_lastname}!\nФотографии с вашей смены вы можете скачать по [ссылке](https://e.pcloud.link/publink/show?code=VZFMtgZFcGtAjmeSKSt5WtESn1djLkxWbPy)", disable_web_page_preview=True, parse_mode="Markdown")
      # Send the review to the specified address
      bot.send_message(chat_id, f"Новый отзыв от {user_name} {user_lastname}:\n{review}")
      user_states[message.chat.id] = "done"
  else:
    bot.send_message(message.chat.id, "Чтобы начать, используйте команду /start.")

# Starting the bot
bot.polling(none_stop=True)
