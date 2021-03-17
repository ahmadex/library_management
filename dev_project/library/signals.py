from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from dev_project.settings import EMAIL_HOST_USER
from library.models import User


@receiver(post_save, sender=User)
def user_created_handler(sender,instance,created,**kwargs):

    if created:
        reciver = instance.email
        subject = 'Signals Testing'
        message = f'Thank You {instance.username} for Registration'
        recepient = str(reciver)        
        send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        
    else:
        reciver = instance.email
        subject = 'Signals Testing'
        message = f'Thank You {instance.username} your Details has been Sucessfully Updated'
        recepient = str(reciver)        
        send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False)



