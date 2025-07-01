import discord
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("TOKEN")
target_user_id = os.getenv("TARGET_USER_ID")

intents = discord.Intents.default()
intents.members = True  # Required to fetch users

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

    try:
        user = await client.fetch_user(target_user_id)
        await user.send("Hello, world!")
        print(f"Sent message to {user}")
    except Exception as e:
        print(f"Failed to send message: {e}")

    await client.close()  # Optional: close bot after sending

client.run(token)