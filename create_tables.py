import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()
db_pass = os.getenv('DB_PASS')
conn = psycopg2.connect(database="soft2db",
                        host="localhost",
                        user="postgres",
                        password=db_pass,
                        port="8000")

cursor = conn.cursor()
cursor.execute('''
               CREATE TABLE IF NOT EXISTS users (
                   id serial primary key,
                   discord_id varchar(30),
                   username varchar(50)
               );
               CREATE TABLE IF NOT EXISTS keywords (
                   id serial primary key,
                   user_id int references users(id),
                   key_string varchar(100)
               );
               CREATE TABLE IF NOT EXISTS drops (
                   id serial primary key,
                   created_at timestamp,
                   guild_id varchar(30),
                   channel_id varchar(30),
                   image_url varchar(100)
               );''')

# cursor.execute('DROP TABLE users CASCADE')
# cursor.execute('DROP TABLE drops')
# cursor.execute('DROP TABLE keywords')
conn.commit()

# cursor.execute('SELECT * FROM users')
# print(cursor.fetchall())
