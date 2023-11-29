import psycopg2


class DatabaseCon:
    def __init__(self, name, host, user, password, port):
        self.name = name
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(
            database=self.name,
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port
        )

    def close(self):
        self.connection.commit()
        self.connection.close()
        self.connection = None

    def get_cursor(self):
        if not self.connection:
            self.connect()
        return self.connection.cursor()

    def get_objects(self, select_query):
        cursor = self.get_cursor()
        cursor.execute(select_query)
        return cursor.fetchall()

    def save_object(self, insert_query):
        cursor = self.get_cursor()
        cursor.execute(insert_query)
        self.close()

    def get_user_id(self, discord_id):
        cursor = self.get_cursor()
        cursor.execute(f"SELECT id FROM users WHERE discord_id = '{discord_id}'")
        return cursor.fetchone()

    def get_users(self):
        return self.get_objects(f'SELECT * FROM users')

    def get_images(self):
        return self.get_objects(f"SELECT * FROM drops")

    def get_user_keywords(self, user_id):
        return self.get_objects(f"SELECT key_string FROM keywords WHERE user_id = '{user_id}'")

    def save_user(self, discord_id, username):
        self.save_object(f'''
            INSERT INTO users (discord_id, username) 
            VALUES('{discord_id}', '{username}')
        ''')

    def save_keyword(self, discord_id, keyword):
        user_id = self.get_user_id(discord_id)[0]
        self.save_object(f'''
            INSERT INTO keywords (user_id, key_string) 
            VALUES('{user_id}', '{keyword}')
        ''')

    def delete_keyword(self, discord_id, keyword):
        user_id = self.get_user_id(discord_id)[0]
        self.save_object(f'''
            DELETE FROM keywords  
            WHERE user_id = '{user_id}' AND key_string = '{keyword}'
        ''')

    def save_image(self, created_at, guild_id, channel_id, image_url):
        self.save_object(f'''
            INSERT INTO drops (created_at, guild_id, channel_id, image_url) 
            VALUES('{created_at}', '{guild_id}', '{channel_id}', '{image_url}')
        ''')
