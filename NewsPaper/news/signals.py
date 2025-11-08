from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post, Category
from .tasks import send_new_post_notification, send_bulk_post_notifications


@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == "post_add":
        subscribers_dict = {}

        for category in instance.category.all():
            for subscriber in category.subscribers.all():
                if subscriber.email not in subscribers_dict:
                    subscribers_dict[subscriber.email] = {
                        'email': subscriber.email,
                        'username': subscriber.username,
                        'post_title': instance.title,
                        'post_text': instance.text,
                        'post_url': instance.get_absolute_url_with_domain()
                    }

        notifications_data = list(subscribers_dict.values())
        if notifications_data:
            send_bulk_post_notifications.delay(notifications_data)