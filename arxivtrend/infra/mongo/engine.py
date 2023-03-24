from mongoengine import connect
from arxivtrend.env import env


connect(
    db=env.MONGO_DB_NAME,
    username="root",
    password="password",
    host=env.MONGO_HOST,
    port=env.MONGO_PORT,
    authentication_mechanism='SCRAM-SHA-1',
    authentication_source='admin'
)
