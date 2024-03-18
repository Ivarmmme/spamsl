import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

# Initialize Pyrogram client
bot = Client(
    "SpamBot",
    bot_token=os.environ["BOT_TOKEN"],
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"]
)

# Global flag to control spamming
is_spamming = False

# Define the spam command handler
@bot.on_message(filters.command(["spam"]))
async def spam_command_handler(client, message):
    global is_spamming
    if is_spamming:
        await message.reply_text('Already spamming. Please wait or use /stop to halt.')
        return
    if len(message.command) > 1:
        custom_message = " ".join(message.command[1:])
        is_spamming = True
        await send_spam_messages(client, message.chat.id, custom_message)
    else:
        await message.reply_text("Please include a message to spam. For example: /spam Hello there!")

# Define the stop command handler
@bot.on_message(filters.command(["stop"]))
async def stop_command_handler(client, message):
    global is_spamming
    is_spamming = False
    await message.reply_text('Spamming stopped. The bot is now silent.')

# Function to send spam messages
async def send_spam_messages(client, chat_id, message):
    global is_spamming
    while is_spamming:
        try:
            await client.send_message(chat_id, text=message)
            await asyncio.sleep(1)  # Sleep duration to respect the rate limit
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            print(f"An error occurred: {e}")
            break

# Start the bot
bot.run()
