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

    def get_users(self):
        return self.get_objects(f'SELECT * FROM users')

    def get_images(self):
        return self.get_objects(f"SELECT * FROM drops")

    def get_user_keywords(self, user_id):
        return self.get_objects(f"SELECT key_string FROM keywords WHERE user_id = '{user_id}'")

    def save_image(self, created_at, guild_id, channel_id, image_url):
        cursor = self.get_cursor()
        cursor.execute(f'''
        INSERT INTO drops (created_at, guild_id, channel_id, image_url) 
        VALUES('{created_at}', '{guild_id}', '{channel_id}', '{image_url}')
        ''')
        self.close()
