import discord
from dotenv import load_dotenv
import os

from agents.A1 import evaluator_A1, examiner_A1

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_USER_ID = int(os.getenv("TARGET_USER_ID"))

intents = discord.Intents.default()
intents.message_content = True  # Needed to read user messages
intents.dm_messages = True  # Needed for DMs

client = discord.Client(intents=intents)

number_of_questions = 5

# Tracking user progress
question_index = 0

latest_question = ""


@client.event
async def on_ready():
    global question_index, latest_question
    print(f'Logged in as {client.user}')
    user = await client.fetch_user(TARGET_USER_ID)

    try:
        result = examiner_A1.app.invoke({})
        await user.send(result["question"])
        latest_question = result["question"]
        question_index = 1  # Next question to ask
    except Exception as e:
        print(f"Failed to send first question: {e}")


@client.event
async def on_message(message):
    global question_index, latest_question
    if message.author.bot:  # if message from evaluator
        return

    # Only handle DMs from the target user
    if isinstance(message.channel, discord.DMChannel) and message.author.id == TARGET_USER_ID:

        if latest_question != "":  # handle user's answer
            user_answer = message.content
            evaluator_result = evaluator_A1.app.invoke({'question': latest_question, 'answer': user_answer})
            await message.channel.send(evaluator_result["evaluation"])

        if question_index < number_of_questions:  # proceed to the next question
            examiner_result = examiner_A1.app.invoke({})
            await message.channel.send(examiner_result["question"])
            latest_question = examiner_result["question"]
            question_index += 1
        else:
            await message.channel.send("Thanks for answering all the questions!")
            await client.close()


if __name__ == '__main__':
    client.run(TOKEN)
