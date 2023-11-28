import discord
import os
import pytesseract
from dotenv import load_dotenv
from database import DatabaseCon


load_dotenv()

pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_PATH')
db_pass = os.getenv('DB_PASS')
BOT_TOKEN = os.getenv("BOT_TOKEN")

db = DatabaseCon('soft2db', 'localhost', 'postgres', db_pass, 8000)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author.name != 'Karuta' and message.author.name != 'ruifag':
        return

    if "dropping" in message.content and 'cards' in message.content:
        # users_to_mention = ['363399227751006218']
        # mention_message = 'Free cards!'
        # for user in users_to_mention:
        #     mention_message += f'<@{user}> '
        created_at = str(message.created_at)[:23]
        guild_id = message.guild.id
        channel_id = message.channel.id
        image_name = message.id
        for att in message.attachments:
            db.save_image(created_at, guild_id, channel_id, image_name)
            await att.save(f'drop_images/{image_name}.png')
        # await message.channel.send(mention_message)
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
