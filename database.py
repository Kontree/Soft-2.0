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

    def save_image(self, created_at, guild_id, channel_id, image_url):
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute(f'''
        INSERT INTO drops (created_at, guild_id, channel_id, image_url) 
        VALUES('{created_at}', '{guild_id}', '{channel_id}', '{image_url}')
        ''')
        self.close()
