from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings
from twilio.rest import Client
import json
from .models import Category, Product

@receiver(post_save, sender=Category)
@receiver(post_save, sender=Product)
def send_sms_on_creation(sender, instance, created, **kwargs):
    if created:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = f"A new {sender.__name__.lower()} named {instance.name} has been created."
        client.messages.create(
            to="user_phone_number",  # Replace with actual recipient phone number
            from_=settings.TWILIO_PHONE_NUMBER,
            body=message,
        )

@receiver(pre_delete, sender=Product)
@receiver(pre_delete, sender=Category)
def save_deleted_to_json(sender, instance, **kwargs):
    data = {
        "name": instance.name,
        "id": instance.id,
    }
    file_path = f'{sender.__name__.lower()}_deleted.json'
    with open(file_path, 'a') as file:
        json.dump(data, file)
        file.write("\n")
