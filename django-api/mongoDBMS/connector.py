import os
import pymongo
from django.conf import settings

"""
class for creating mongo client connection for profiles collection
"""
class ProfileDBConnector:

    def __init__(self):
        connectionData: dict = settings.MONGO_CONNECTION_INFO
        self.MONGO_SRV: str = connectionData['MONGO_SRV']
        self.MONGO_PORT: int = connectionData['MONGO_PORT']
        self.MONGO_USERNAME: str = connectionData['MONGO_USERNAME']
        self.MONGO_PASSWORD: str = connectionData['MONGO_PASSWORD']
        self.DB: str = connectionData['DB']
        self.COL: str = connectionData['COL']

    """singleton object because works with database"""
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    """establish and returns connection of mongo database"""
    def connect(self):
        mongoSrv = pymongo.MongoClient(f"mongodb://{self.MONGO_USERNAME}:{self.MONGO_PASSWORD}@{self.MONGO_SRV}:{self.MONGO_PORT}/")
        mongoDB = mongoSrv[self.DB]
        mongoCOL = mongoDB[self.COL]
        connection = {
            'mongoSrv': mongoSrv,
            'mongoCOL': mongoCOL

        }
        return connection


"""
contextmanager class for open mongo connection at
enter and close it when the work is done and exit
 """
class ProfileDBClientGenerator:

    def __enter__(self):
        self.client = ProfileDBConnector().connect()
        return self.client['mongoCOL']

    def __exit__(self, *args):
        self.client['mongoSrv'].close()

