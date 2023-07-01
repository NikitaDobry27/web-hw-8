from mongoengine import connect
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongo_pass = config.get('DB', 'pass')
mongo_db_name = config.get('DB', 'db_name')
mongo_domain = config.get('DB', 'domain')


connect(
    host=f"mongodb+srv://{mongo_user}:{mongo_pass}@{mongo_domain}/{mongo_db_name}?retryWrites=true&w=majority", ssl=True
)
