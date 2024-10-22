import json
import os
import openai
from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv
import discord

load_dotenv()


intents = discord.Intents.all()

intents.messages = True
intents.message_content = True

discord_client = discord.Client(intents=intents)

OFFENSE_CATEGORY=(
    "offensive", 
    "sexual", 
    "neutral", 
    "self-promotion"
)

COMMUNITY_GIDELINES = f"""
Below is a post being submitted to a forum.
Your task is to determine whether the post follows the following community guidelines, using context to ensure accurate classification. If the post is in a language other than English, focus on identifying whether the content violates any of the guidelines rather than flagging it solely for being in a different language.

Do's:
Share respectful, constructive, and informative content.
Promote educational content specifically related to technology.
Engage with others positively and stay on topic.

Don'ts:
Offensive Content: Do not post anything that is offensive in nature, including hateful, discriminatory, or harassing language.
Sexual Content: Do not post anything that is sexual in nature, including explicit or suggestive material.
Self-Promotion: Do not post any form of self-promotion, except for educational technology-related content.
Return one of [{','.join(OFFENSE_CATEGORY)}] based on whether the post follows the rules. Be sure to account for context before classifying content as offensive or inappropriate.
"""

@dataclass
class Prompt:
    role:str
    content:str

    def format(self):

        return self.__dict__
    
@dataclass
class Messages:

    messages:List[Prompt]

    def format(self):

        return [message.format() for message in self.messages]
    
def _ask_gpt(messages:Messages)->str:

    completion = client.chat.completions.create(
        model='gpt-4-1106-preview',
        messages=messages.format(),
    )
    content = completion.choices[0].message.content
    return content


def _welcome_member(username, servername):

    prompt = f"Create a fun and quirky welcome message for {username} who has joined the {server_name} server."

    response = client.completions.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )

    return response.choices[0].text.strip()

def __prepare_messages(user_messages:str):

    system = Prompt(
        role="system",
        content=COMMUNITY_GIDELINES
    )

    user_prompt = Prompt(
        role="user",
        content=user_messages
    )

    messages = Messages(
        messages=[
            system,
            user_prompt
        ]
    )

    return messages

async def act(message, offense_category):

    if offense_category == "neutral":
        return
    
    await message.delete()
    await message.channel.send(f"{message.author.mention} - your message was removed for violating the community guidelines.")

@discord_client.event
async def on_ready():
    print(f'Logged in as {discord_client.user}')


@discord_client.event
async def on_message(message):

    if message.author == discord_client.user:

        return

    messages = __prepare_messages(user_messages=message.content)
    
    offense_category = _ask_gpt(messages=messages)

    await act(message=message, offense_category=offense_category)

@discord_client.event
async def on_message_edit(before, after):

    offense = _ask_gpt(messages=__prepare_messages(user_messages=after.content))

    print(offense)

    print(before.content)

    print(after.content)

    await act(message=after, offense_category=offense)


@discord_client.event
async def on_member_join(member):

    welcome_message = _welcome_member(member.name, member.guild.name)

    channel = discord.utils.get(member.guild.channels, name="general")

    if channel:

        await channel.send(welcome_message)


if __name__ == "__main__":

    open_ai_key = os.environ.get("open_ai_key")

    discord_token = os.environ.get("discord_token")

    assert all((
        open_ai_key is not None and open_ai_key != "", 
        discord_token is not None and discord_token != "",
    )), "Token and OpenAI key are required."

    client = openai.OpenAI(api_key=os.environ.get("open_ai_key"))


    discord_client.run(discord_token)