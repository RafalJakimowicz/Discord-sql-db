import discord
import os
from bot import LoggingBot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.messages = True  # Enable message intents
intents.guilds = True
intents.members = True
intents.message_content = True
bot = LoggingBot(command_prefix='!', intents=intents)

@bot.command()
async def goodbye(ctx):
    await ctx.send(f"Goodbye {ctx.author.name}")

bot.run(TOKEN)