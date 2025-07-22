import discord
from dotenv import load_dotenv
import os

from agents import agent, evaluator

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_USER_ID = int(os.getenv("TARGET_USER_ID"))

intents = discord.Intents.default()
intents.message_content = True  # Needed to read user messages
intents.dm_messages = True  # Needed for DMs

client = discord.Client(intents=intents)

# Tracking user progress
number_of_questions = 5
question_index = 0

question = ""
dialogue = ""
topic = ""


@client.event
async def on_ready():
    global question_index, question, dialogue, topic
    print(f'Logged in as {client.user}')
    user = await client.fetch_user(TARGET_USER_ID)

    try:
        agent_result = agent.app.invoke({})
        dialogue = agent_result["dialogue"]
        await user.send(dialogue)

        question = agent_result["question"]
        await user.send(question)

        topic = agent_result["topic"]

        question_index = 1
    except Exception as e:
        print(f"Failed to send first question: {e}")


@client.event
async def on_message(message):
    global question_index, question
    if message.author.bot:  # if message from generator, examiner or evaluator
        return

    # Only handle DMs from the target user
    if isinstance(message.channel, discord.DMChannel) and message.author.id == TARGET_USER_ID:

        if question != "":  # handle user's answer
            user_answer = message.content
            evaluator_result = evaluator.app.invoke(
                {'dialogue': dialogue, 'question': question, 'answer': user_answer, 'topic': topic})
            await message.channel.send(evaluator_result["evaluation"])

        if question_index < number_of_questions:  # proceed to the next question
            # TODO
            question_index += 1
            pass
        else:
            await message.channel.send("Thanks for answering all the questions!")
            await client.close()


if __name__ == '__main__':
    client.run(TOKEN)
