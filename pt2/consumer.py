import pika
from mongoengine import *


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


def send_email(email):
    print(f"Sending email to {email}...")
    print("Email sent!")


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="email_queue")


def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects(id=contact_id).first()
    if contact and not contact.message_sent:
        send_email(contact.email)
        contact.message_sent = True
        contact.save()


channel.basic_consume(queue="email_queue", on_message_callback=callback, auto_ack=True)

print("Waiting for messages...")
channel.start_consuming()
