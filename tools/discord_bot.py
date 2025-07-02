import discord
import asyncio
from dotenv import load_dotenv
import os

from agents import examiner

load_dotenv()

TOKEN = os.getenv("TOKEN")
TARGET_USER_ID = int(os.getenv("TARGET_USER_ID"))

intents = discord.Intents.default()
intents.message_content = True  # Needed to read user messages
intents.dm_messages = True  # Needed for DMs

client = discord.Client(intents=intents)

number_of_questions = 5

# Tracking user progress
question_index = 0


@client.event
async def on_ready():
    global question_index
    print(f'Logged in as {client.user}')
    user = await client.fetch_user(TARGET_USER_ID)

    try:
        result = examiner.app.invoke({})
        await user.send(result["question"])
        question_index = 1  # Next question to ask
    except Exception as e:
        print(f"Failed to send first question: {e}")


@client.event
async def on_message(message):
    global question_index
    if message.author.bot:  # if message from evaluator
        return

    # Only handle DMs from the target user
    if isinstance(message.channel, discord.DMChannel) and message.author.id == TARGET_USER_ID:

        if question_index < number_of_questions:
            result = examiner.app.invoke({})
            await message.channel.send(result["question"])
            question_index += 1
        else:
            await message.channel.send("Thanks for answering all the questions!")
            await client.close()  # Instead of exit()


if __name__ == '__main__':
    client.run(TOKEN)
