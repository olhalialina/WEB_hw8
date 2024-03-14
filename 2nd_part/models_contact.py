from mongoengine import Document
from mongoengine.fields import StringField, EmailField, BooleanField
from mongoengine import connect

connect(
    db="web20",
    host="mongodb+srv://goitlearn:******@goitlearn.w7mvfnf.mongodb.net/?retryWrites=true&w=majority&appName=goitlearn",
    tls=True,
    tlsInsecure=True,
)


class Contact(Document):
    fullname = StringField(max_length=150, required=True, unique=True)
    address = StringField(max_length=150)
    email = EmailField(max_length=100)
    phone = StringField(max_length=30)
    message_sent = BooleanField(default=False)
    preferred_contact_method = StringField(choices=["email", "sms", "pigeon"], default="email")
    meta = {"collection": 'contacts'}
