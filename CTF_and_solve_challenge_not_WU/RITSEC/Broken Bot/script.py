from telegram.ext import Updater, CommandHandler

# Define your command handler functions here


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hello, I'm a bot!")


def help(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="This is a help message.")


# Create an Updater object and attach your command handlers to it
updater = Updater(
    token='6055124896:AAFyQlC_8dr1GndB26ji4iV2ol2bPPQ9lq4', use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))

# Get the list of commands for your bot
commands = list(updater.dispatcher.commands)
print(commands)
