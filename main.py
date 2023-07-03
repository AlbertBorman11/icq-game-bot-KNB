#!/usr/bin/env python
from bot.bot import Bot
from bot.handler import BotButtonCommandHandler
from bot.handler import MessageHandler
from bot.filter import Filter
import json
import random

"""
This game is called KNB, because the stone in Russian begins with K, scissors with H and Bauman with B
"""

TOKEN = "" # Token from @metabot (ICQ)

# Create a Bot instance
bot = Bot(token=TOKEN)

# Path to the database file
db_folder = "db.txt"

# Admin ID
admin_id = ""

# Choices for the game
options = ["🪨", "✂️", "📃"]

# Inline keyboard markup for different scenarios
return_kb = [[{"text": "Play again?", "callbackData": "start"}]]
game_kb = [[{"text": "PLAY!", "callbackData": "start"}]]
knb_kb = [
    [{"text": options[0], "callbackData": "k"}, {"text": options[1], "callbackData": "n"}],
    [{"text": options[2], "callbackData": "b"}]
]
admin_kb = [[{"text": "Statistics", "callbackData": "stat"}]]


def message_callback(bot, event):
    # Read the existing user IDs from the database
    with open(db_folder, 'r') as file:
        data = file.read()

    # Check if the user is already in the database
    if event.data['from']['userId'] not in data:
        with open(db_folder, 'a') as file:
            file.write(f"{event.data['from']['userId']}\n")

        # Send a welcome message to the new user
        bot.send_text(chat_id=event.from_chat, text=f"Hello {event.data['from']['firstName']}! This is a bot for playing Rock, Paper, Scissors. To start the game, type '.game'. To get information about the bot, type '.help'")

    # Get the user's last name
    last_name = event.data['from'].get('lastName', 'Null')

    # Get the user's username
    username = event.data['from'].get('nick', 'Null')

    if event.text == '.help':
        # Send help message to the user
        bot.send_text(chat_id=event.from_chat, text=f"Welcome! This bot plays Rock, Paper, Scissors with you. It's all based on pure randomness. The bot was created by @gargamelix. If you need help with creating bots, deploying them to hosting, or just want to suggest an update, feel free to ask! The administrator also has a channel where he shares updates and new bots. Follow @gofex. To start the game, type '.game'\n\nAdditional information about you:\nID: {event.data['from']['userId']}\nFirst name: {event.data['from']['firstName']}\nLast name: {last_name}\nUsername: {username}")

    if event.text == '.game':
        # Send the game prompt to the user
        bot.send_text(chat_id=event.from_chat, text="Let's play?", inline_keyboard_markup=json.dumps(game_kb))

    if admin_id == event.data['from']['userId']:
        if event.text == ".admin":
            # Send admin options to the admin user
            bot.send_text(chat_id=event.from_chat, text="Hello Administrator!", inline_keyboard_markup=json.dumps(admin_kb))


def start(bot, event):
    # Send the game options to the user
    bot.send_text(chat_id=event.from_chat, text=f"{event.data['from']['firstName']}, choose", inline_keyboard_markup=json.dumps(knb_kb))


def stat(bot, event):
    # Read the database and count the number of registered users
    with open(db_folder, 'r') as file:
        num_users = len(file.readlines())

    # Send the statistics to the user
    bot.send_text(chat_id=event.from_chat, text=f"The bot currently has {num_users} registered users")

# 😵 It's a necessary measure

def k(bot, event):
    game(bot, event, "🪨")

def n(bot, event):
    game(bot, event, "✂️")

def b(bot, event):
    game(bot, event, "📃")


def game(bot, event, user_choice):
    # Randomly choose the computer's choice
    computer_choice = random.choice(options)

    # Send the user's choice and computer's choice to the user
    bot.send_text(chat_id=event.from_chat, text=f"{event.data['from']['firstName']} chose {user_choice}, and the computer chose {computer_choice}.")
    # It's a tie
    if user_choice == computer_choice: bot.send_text(chat_id=event.from_chat, text="It's a tie! Try again.", inline_keyboard_markup=json.dumps(return_kb))
    # The user wins
    elif (user_choice == "🪨" and computer_choice == "✂️") or (user_choice == "✂️" and computer_choice == "📃") or (user_choice == "📃" and computer_choice == "🪨"): bot.send_text(chat_id=event.from_chat, text=f"{event.data['from']['firstName']} wins! Congratulations!", inline_keyboard_markup=json.dumps(return_kb))
    # The computer wins
    else: bot.send_text(chat_id=event.from_chat, text="The computer wins! Try again.", inline_keyboard_markup=json.dumps(return_kb))


# Add message and button handlers to the bot's dispatcher
bot.dispatcher.add_handler(MessageHandler(callback=message_callback))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=start, filters=Filter.callback_data("start")))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=stat, filters=Filter.callback_data("stat")))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=k, filters=Filter.callback_data("k")))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=n, filters=Filter.callback_data("n")))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=b, filters=Filter.callback_data("b")))

# Start the bot
bot.start_polling()
bot.idle()
