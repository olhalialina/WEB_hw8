import faker
from random import randint

import pika

from models_contact import Contact

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='send_contact', exchange_type='topic')
channel.queue_declare(queue='email_queue', durable=True)
channel.queue_declare(queue='sms_queue', durable=True)
channel.queue_declare(queue='pigeon_queue', durable=True)
channel.queue_bind(exchange='send_contact', queue='email_queue', routing_key='email')
channel.queue_bind(exchange='send_contact', queue='sms_queue', routing_key='sms')
channel.queue_bind(exchange='send_contact', queue='pigeon_queue', routing_key='pigeon')


def main():
    fake = faker.Faker("uk-Ua")
    for _ in range(12):
        fake_name = fake.name()
        fake_address = fake.address()
        fake_email = fake.email()
        fake_phone_number = '+380' + str(randint(111111111, 999999999))
        preferred_contact_method = fake.random_element(elements=("email", "sms", "pigeon"))

        contact = Contact(fullname=fake_name,
                          address=fake_address,
                          email=fake_email,
                          phone=fake_phone_number,
                          preferred_contact_method=preferred_contact_method).save()

        channel.basic_publish(
            exchange='send_contact',
            routing_key=preferred_contact_method,
            body=str(contact.id).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(f" [x] Send message to {contact.fullname} via {preferred_contact_method}")
    connection.close()


if __name__ == '__main__':
    main()