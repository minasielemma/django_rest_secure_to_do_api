from django.db.models.signals import post_init
from django.dispatch import receiver
from .models import Plan, Task

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