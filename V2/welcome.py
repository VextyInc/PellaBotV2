import discord
from config import TARGET_CHANNEL_ID

async def send_welcome_message(member, bot):
    # Fetch the target channel
    channel = bot.get_channel(TARGET_CHANNEL_ID)

    if channel:
        # Send the welcome message as a reply to the member's join message
        welcome_message = (
            f"🎉 Welcome to the Server! 🎉\n\n"
            f"Hi there! I'm {bot.user.name} Made By TheUselessCreator, one of the moderators and staff members here. 😊 "
            f"Our awesome owner is Stonechat.\n\n"
            f"If you need any help or have questions, feel free to reach out to me or any of the staff. We're here to make sure you have a great time!\n\n"
            f"Check out our cool features and make sure to visit [pella.app](https://pella.app) for more fun! 🎮✨\n\n"
            f"Enjoy your stay and have a blast! 🚀"
        )

        # Search for the member's join message and reply to it
        async for message in channel.history(limit=10):
            if message.author == member:
                await message.reply(welcome_message, mention_author=True)
                break
