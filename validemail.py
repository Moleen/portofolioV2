
from pymongo import MongoClient

client = MongoClient('mongodb+srv://maulanasyakhiya:X6Tx5vkB5TZUiCMo@cluster0.zsgjrxk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0', serverSelectionTimeoutMS = 500)
db = client.portofolio


try:
    if client.server_info():
        pass
        print("db conected")
except:
    print("db not connect")