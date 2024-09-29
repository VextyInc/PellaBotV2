import discord
from discord.ext import commands
import json
from config import DISCORD_TOKEN, TARGET_CHANNEL_ID
from data_handler import load_data, find_best_answer, save_new_data
from anti_nsfw import check_for_offenses
from logger import log_message, process_logged_messages
from ai_learning import self_improve, update_model
from welcome import send_welcome_message

# Load datasets
dataset1 = load_data('data/PellaData1.json')
dataset2 = load_data('data/PellaData2.json')
datasets = [dataset1, dataset2]

# Create a bot instance with proper intents
intents = discord.Intents.default()
intents.members = True  # Enable members intent to track new members
intents.messages = True
intents.message_content = True  # Ensure message content can be processed
bot = commands.Bot(command_prefix='!', intents=intents)

# Log all messages to a file for future processing
LOG_FILE = 'data/message_log.txt'
PROCESSED_DATA_FILE = 'data/ai_gen_data.txt'
RL_FILE = 'data/reinforcement_learning.json'

# Initialize reinforcement learning memory (feedback system) from the JSON file
def load_rl_memory():
    try:
        with open(RL_FILE, 'r') as file:
            rl_memory = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, initialize the memory with default values
        rl_memory = {
            "positive_feedback": 0,
            "negative_feedback": 0,
            "successful_answers": 0,
            "failed_answers": 0
        }
        # Save the initialized memory to the file
        with open(RL_FILE, 'w') as file:
            json.dump(rl_memory, file, indent=4)
    return rl_memory

# Load reinforcement learning memory
rl_memory = load_rl_memory()

# Thresholds for AI improvement based on feedback
IMPROVEMENT_THRESHOLD = 10

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.event
async def on_member_join(member):
    """Handles welcoming a new member and replying to the join message"""
    await send_welcome_message(member, bot)

@bot.event
async def on_message(message):
    if message.channel.id == TARGET_CHANNEL_ID:
        if not message.author.bot:  # Ignore messages from the bot itself

            # Log the message for future reference
            log_message(message.content, message.author.id, message.channel.id, LOG_FILE)

            # Check for NSFW content and behavior tracking
            warning_message = check_for_offenses(message, message.author.id)
            if warning_message:
                await message.channel.send(warning_message)
                return  # Skip further processing for this message

            # Smart AI Model: Try to find the best answer
            question = message.content
            answer, confidence = find_best_answer(question, datasets)

            if answer:
                # Give the answer with feedback request
                response = await message.channel.send(f"{answer}\n\nWas this helpful? Please react with 👍 or 👎.")
                await response.add_reaction('👍')
                await response.add_reaction('👎')
                
                # Track AI performance in reinforcement learning
                await self_improve(response, rl_memory, message.channel)
                
                if rl_memory["positive_feedback"] - rl_memory["negative_feedback"] >= IMPROVEMENT_THRESHOLD:
                    await update_model(datasets)  # Improve AI if it receives enough positive feedback
            else:
                await message.channel.send("Could you give me more context so I can help answer your question?")
                rl_memory["failed_answers"] += 1

            # Process logged messages periodically for new data ingestion
            process_logged_messages(LOG_FILE, PROCESSED_DATA_FILE, datasets)

    await bot.process_commands(message)

@bot.command()
async def processed_data(ctx):
    """
    Command to fetch the processed data from the ai_gen_data.txt file.
    """
    with open(PROCESSED_DATA_FILE, 'r') as file:
        processed_data = file.read()
    if processed_data:
        await ctx.send(f"Processed Data:\n```{processed_data}```")
    else:
        await ctx.send("No processed data available yet.")

@bot.command()
async def feedback(ctx):
    """
    Command to show reinforcement learning stats (feedback received by the AI).
    """
    with open(RL_FILE, 'r') as file:
        feedback_data = json.load(file)
    feedback_msg = (
        f"AI Feedback Stats:\n"
        f"Positive Feedback: {feedback_data['positive_feedback']}\n"
        f"Negative Feedback: {feedback_data['negative_feedback']}\n"
        f"Successful Answers: {feedback_data['successful_answers']}\n"
        f"Failed Answers: {feedback_data['failed_answers']}"
    )
    await ctx.send(feedback_msg)

# Run the bot
bot.run(DISCORD_TOKEN)
