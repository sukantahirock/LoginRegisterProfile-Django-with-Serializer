from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import User, Profile

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Our Site!'
        html_message = render_to_string('accounts/welcome_email.html', {
            'user': instance
        })
        plain_message = strip_tags(html_message)
        send_mail(
            subject,
            plain_message,
            None,  # Uses DEFAULT_FROM_EMAIL
            [instance.email],
            html_message=html_message,
            fail_silently=False,
        )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(pre_save, sender=Profile)
def notify_profile_update(sender, instance, **kwargs):
    if instance.pk:  # Only for updates, not creation
        old_profile = Profile.objects.get(pk=instance.pk)
        if old_profile.bio != instance.bio:
            subject = 'Your profile has been updated'
            message = f'Your profile bio was updated from "{old_profile.bio}" to "{instance.bio}"'
            send_mail(
                subject,
                message,
                None,
                [instance.user.email],
                fail_silently=False,
            )