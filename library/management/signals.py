from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile,StudentProfile

@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created,  **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_userprofile(sender, instance, **kwargs):
   instance.userprofile.save()


@receiver(post_save, sender=User)
def create_studentprofile(sender, instance, created,  **kwargs):
    if created:
      StudentProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_studentprofile(sender, instance, **kwargs):
    instance.userprofile.save()
    