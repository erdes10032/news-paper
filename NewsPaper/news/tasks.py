from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from .models import Post, Category


@shared_task
def send_new_post_notification(email, username, post_title, post_text, post_url):
    html_content = render_to_string('post_created.html', {
        'post_title': post_title,
        'post_text': post_text,
        'username': username,
        'post_url': post_url
    })

    msg = EmailMultiAlternatives(
        subject=post_title,
        body=f'Hello, {username}. New article in your favorite section!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return f"Email sent to {email}"


@shared_task
def send_bulk_post_notifications(notifications_data):
    results = []
    for notification in notifications_data:
        result = send_new_post_notification.delay(
            notification['email'],
            notification['username'],
            notification['post_title'],
            notification['post_text'],
            notification['post_url']
        )
        results.append(result)
    return f"Scheduled {len(results)} email tasks"


@shared_task
def send_weekly_articles():
    week_ago = datetime.now() - timedelta(days=7)
    categories = Category.objects.all()

    for category in categories:
        recent_posts = Post.objects.filter(
            category=category,
            creation_date__gte=week_ago
        ).distinct()

        if not recent_posts:
            continue

        subscribers = category.subscribers.all()
        for subscriber in subscribers:
            html_content = render_to_string('weekly_articlesletter.html', {
                'username': subscriber.username,
                'category': category,
                'posts': recent_posts,
                'week_ago': week_ago
            })

            msg = EmailMultiAlternatives(
                subject=f'Weekly news selection in the category "{category.name}"',
                body=f'Hello, {subscriber.username}! Here are the new articles'
                     f' in the category "{category.name}" for the past week.',
                from_email='erdes3182@yandex.ru',
                to=[subscriber.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

    return 'Successfully sent weekly emails'