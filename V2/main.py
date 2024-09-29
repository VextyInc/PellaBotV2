import discord
from discord.ext import commands
from config import DISCORD_TOKEN, TARGET_CHANNEL_ID
from data_handler import load_data, find_best_answer
from message_formatter import format_logged_messages

# Load datasets
dataset1 = load_data('data/PellaData1.json')
dataset2 = load_data('data/PellaData2.json')
datasets = [dataset1, dataset2]

# Create a bot instance
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.event
async def on_message(message):
    # Check if the message is from the target channel
    if message.channel.id == TARGET_CHANNEL_ID:
        if not message.author.bot:  # Ignore messages from the bot itself
            # Log the message
            with open('data/ai_gen_data.txt', 'a') as log_file:
                log_file.write(f"{message.content}\n")

            question = message.content
            answer = find_best_answer(question, datasets)

            if answer:
                await message.channel.send(answer)
            else:
                await message.channel.send("Could you give me more context so I can help answer your question?")

    await bot.process_commands(message)

@bot.command()
async def format_messages(ctx):
    format_logged_messages()
    await ctx.send("Messages have been formatted and saved.")

# Run the bot
bot.run(DISCORD_TOKEN)
