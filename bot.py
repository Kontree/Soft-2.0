import discord
import os
import cv2
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
    if message.author.name == client.user.name:
        return

    if "dropping" in message.content and 'cards' in message.content:
        created_at = str(message.created_at)[:23]
        guild_id = message.guild.id
        channel_id = message.channel.id
        image_name_id = message.id
        strings = []
        for i, att in enumerate(message.attachments, 1):
            image_name = f'{image_name_id}({i})'
            img_path = f'drop_images/{image_name}/'
            os.mkdir(img_path)
            db.save_image(created_at, guild_id, channel_id, img_path)
            await att.save(f'{img_path}original.png')
            image = cv2.imread(f'{img_path}original.png')
            first = [x1, y1, x2, y2] = 50, 310, 240, 360
            second = [x1, y1, x2, y2] = 320, 310, 510, 360
            third = [x1, y1, x2, y2] = 600, 310, 790, 360
            images = [first, second, third]
            cropped_images = [image[img[1]:img[3], img[0]:img[2]] for img in images]
            for i, image in enumerate(cropped_images, 1):
                try:
                    string = pytesseract.image_to_string(image)
                    string = string.lower()
                except pytesseract.pytesseract.TesseractError:
                    string = f'Something went wrong while reading image'
                strings.append(string)
                with open(f'{img_path}{i}.txt', 'w') as f:
                    f.write(string)

        found = False
        user_ids_to_mention = []
        all_users = [{'id': id, 'disc_id': disc_id} for id, disc_id, name in db.get_users()]
        detected_keywords = {user['disc_id']: [] for user in all_users}
        for user in all_users:
            keywords = [keyword[0] for keyword in db.get_user_keywords(user['id'])]
            for keyword in keywords:
                if any(keyword in string for string in strings):
                    found = True
                    detected_keywords[user['disc_id']].append(keyword)
                    user_ids_to_mention.append(user['disc_id'])
                    break
        if found:
            mention_message = 'Detected something!'
            for user in user_ids_to_mention:
                mention_message += f'\n<@{user}>\n' \
                                   f"\t\t{' '.join(detected_keywords[user])}"
            await message.channel.send(mention_message)


client.run(BOT_TOKEN)
