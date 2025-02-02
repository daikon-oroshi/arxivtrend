from mongoengine import connect
from arxivtrend.env import env


class Connection:
    def connect_db(self):
        return connect(
            db=env.MONGO_DB_NAME,
            username="root",
            password="password",
            host=env.MONGO_HOST,
            port=env.MONGO_PORT,
            authentication_mechanism='SCRAM-SHA-1',
            authentication_source='admin',
            uuidRepresentation='standard'
        )

    def __enter__(self):
        self.conn = self.connect_db()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
