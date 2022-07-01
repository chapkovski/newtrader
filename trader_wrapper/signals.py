from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Event
import json

# @receiver(pre_save, sender=Event)
# def before_event_update(sender, instance,  **kwargs):
# 	instance.body=json.dumps(instance.body)
# 	instance.balance = instance.owner.ending_balance



