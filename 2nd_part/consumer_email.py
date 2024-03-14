import pika
from bson import ObjectId
from models_contact import Contact

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel_email = connection.channel()

channel_email.queue_declare(queue='email_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    pk = body.decode()
    print(f" [x] Received {pk}")
    print(f" [x] Done: {method.delivery_tag}")

    result_of_sending = send_message_to_email()
    if result_of_sending:
        contact = Contact.objects.get(id=ObjectId(pk))
        contact.update(set__message_sent=True)
        contact.save()
        print(f"Email was sent to {contact.fullname}'s email address: {contact.email}")

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel_email.basic_qos(prefetch_count=1)
channel_email.basic_consume(queue="email_queue", on_message_callback=callback)


def send_message_to_email():
    return True


if __name__ == "__main__":
    channel_email.start_consuming()