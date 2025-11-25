from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from app.models import *
from django.core.mail import send_mail
import os
@receiver(post_save,sender=User)
def signals_sending_mail(sender,instance,created,**kwargs):
    if created:
        send_mail(
            'Welcome to Our Site',
            'Thank you for registering with us.',
            'ashutoshkhilar5@gmail.com',
            [instance.email],
            fail_silently=False,
        )
        

@receiver(post_delete,sender=Profile)
def delete_pp(sender,instance,**kwargs):
    if instance.profile_pic:
        filepath=instance.profile_pic.path
        if os.path.isfile(filepath):
            os.remove(filepath)
