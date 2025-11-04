from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post, Category
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == "post_add":
        subscriber_data = {}
        for category in instance.category.all():
            for subscriber in category.subscribers.all():
                subscriber_data[subscriber.email] = subscriber.username
        url = instance.get_absolute_url_with_domain()
        for email, username in subscriber_data.items():
            html_content = render_to_string('post_created.html', {
                'post': instance,
                'username': username,
                'url': url
            })

            msg = EmailMultiAlternatives(
                subject=instance.title,
                body=f'Hello, {username}. New article in your favorite section!',
                from_email='erdes3182@yandex.ru',
                to=[email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

