import pika
from mongoengine import *
from faker import Faker


mongo_user = "someuser"
mongo_pass = "somepass"
mongo_db_name = "somedb"
mongo_domain = "somedomain"

connect(
    host=f"mongodb+srv://{mongo_user}:{mongo_pass}@{mongo_domain}/{mongo_db_name}?retryWrites=true&w=majority",
    ssl=True,
)


class Contact(Document):
    full_name = StringField(required=True)
    email = EmailField(required=True)
    message_sent = BooleanField(default=False)


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="email_queue")


fake = Faker()
for _ in range(100):
    contact = Contact(full_name=fake.name(), email=fake.email())
    contact.save()

    channel.basic_publish(exchange="", routing_key="email_queue", body=str(contact.id))
connection.close()
