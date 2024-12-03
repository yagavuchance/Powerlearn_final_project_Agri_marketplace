from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # Ensure the Profile is saved whenever the User is saved
    if hasattr(instance, 'profile'):  # Prevent the RelatedObjectDoesNotExist error
        instance.profile.save()

