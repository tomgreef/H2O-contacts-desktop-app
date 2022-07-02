from pymongo import MongoClient

# Singleton Design pattern 
class DBConnector(object):

    def __init__(self):
       self.connection = None
       self.client = None

    # creats new connection
    def create_connection(self):
        self.client = MongoClient('mongodb://192.168.1.112:27017')
        self.connection = self.client.h2o
        return self.connection

    # For explicitly opening database connection
    def __enter__(self):
        self.connection = self.create_connection()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

class MongoManager:
    __instance = None

    @staticmethod 
    def getInstance():
        if MongoManager.__instance == None:
            MongoManager()
        return MongoManager.__instance

    def __init__(self):
        if MongoManager.__instance != None:
            raise Exception("This class is a singleton! Use .getInstance()")
        else:
            MongoManager.__instance = DBConnector().create_connection()