from django.db.models.signals import post_init
from django.dispatch import receiver
from .models import Plan, Task
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils.text import slugify
from asgiref.sync import async_to_sync
from functools import partial
from .consumers import NotificationConsumer

@receiver(post_init, sender=Plan)
def increment_fetch_count_plan(sender, instance, **kwargs):
    """
    Signal handler to increment the fetch count when an object is fetched.
    """
    # Increment the fetch count
    if instance.pk:
        instance.fetch_count += 1
        instance.save(update_fields=['fetch_count'])
    
@receiver(post_init, sender=Task)
def increment_fetch_count_task(sender, instance, **kwargs):
    """
    Signal handler to increment the fetch count when an object is fetched.
    """
    # Increment the fetch count
    if instance.pk:
        instance.fetch_count += 1
        instance.save(update_fields=['fetch_count'])

@receiver(post_save, sender=Plan)
def create_plan_channel(sender, instance, created, **kwargs):
    if created:
        # Generate a unique channel name based on the plan_name
        instance.channel_name = f"plan_{slugify(instance.plan_name)}_{instance.id}"
        instance.save()
        
        
@receiver(post_save, sender=Plan)
def send_notification(sender, instance,created, **kwargs):
    if created:
        owner = instance.owner
        message = f"A new plan '{instance.plan_name}' has been created."
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f"user_{owner.id}", {"type": "notify_user", "message": message})