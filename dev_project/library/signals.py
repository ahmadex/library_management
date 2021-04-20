from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from dev_project.settings import EMAIL_HOST_USER
from library.models import User
import datetime


@receiver(pre_save, sender=User)
def befor_user_created(sender, instance,**kwargs):
    if instance.last_login:
        print('pre_save')
        print(instance.last_login)
       

@receiver(post_save, sender=User)
def user_created_handler(sender,instance,created,**kwargs):

    if created:
        print('Register')        
        reciver = instance.email
        subject = 'Signals Testing'
        message = f'Thank You {instance.username} for Registration'
        recepient = str(reciver)        
        send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        
    # else:
    #     date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    #     if str(instance.last_login)[:16] != date_now:
    #         print('user Updation done')
            
    #         if instance.email:
    #             reciver = instance.email
    #             subject = 'Update'
    #             message = f'Thank You {instance.username} for Updation'
    #             recepient = str(reciver)        
    #             send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False)

            