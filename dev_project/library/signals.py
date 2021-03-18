from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from dev_project.settings import EMAIL_HOST_USER
from library.models import User


@receiver(post_save, sender=User)
def user_created_handler(sender,instance,created,**kwargs):

    if created:
        if instance.is_staff:
            print('admin created')
            print(kwargs)
        else:
            print(' Normal User created')
            print(kwargs)
        
        # reciver = instance.email
        # subject = 'Signals Testing'
        # message = f'Thank You {instance.username} for Registration'
        # recepient = str(reciver)        
        # send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        
    else:
        
        if instance.is_staff:
            print('admin Updated')
            print(kwargs)
            
            reciver = instance.email
            subject = 'Signals Testing'
            message = f'Thank You {instance.username} for Updation'
            recepient = str(reciver)        
            send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False)

        else:
            print(' Normal User updated')
            print(kwargs)
            
            if instance.email:
                reciver = instance.email
                subject = 'Signals Testing'
                message = f'Thank You {instance.username} for Updation'
                recepient = str(reciver)        
                send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False)



# Normal User updated
# {'signal': <django.db.models.signals.ModelSignal object at 0x7f33f4e9ceb8>, 'update_fields': frozenset({'last_login'}), 'raw': False, 'using': 'default'}

# admin Updated kwargs
# {'signal': <django.db.models.signals.ModelSignal object at 0x7fa2223d8eb8>, 'update_fields': frozenset({'last_login'}), 'raw': False, 'using': 'default'}    
            
            