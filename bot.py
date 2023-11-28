import discord
from dotenv import load_dotenv
load_dotenv()
from config import BOT_TOKEN


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author.name != 'Karuta':
        return

    if message.content == "I'm dropping 3 cards since this server is currently active!":
        users_to_mention = ['363399227751006218']
        mention_message = 'Free cards!'
        for user in users_to_mention:
            mention_message += f'<@{user}> '
        await message.channel.send(mention_message)
    # for emb in message.embeds:
    #     print(emb.author)
    #     print(emb.colour)
    #     print(emb.description)
    #     print(emb.fields)
    #     print(emb.footer)
    #     print(emb.image)
    #     print(emb.provider)
    #     print(emb.thumbnail)
    #     print(emb.timestamp)
    #     print(emb.title)
    #     print(emb.type)
    #     print(emb.url)
    #     print(emb.video)


client.run(BOT_TOKEN)
