import logging
import logging
from datetime import datetime, timedelta
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from ...models import Post, Category

logger = logging.getLogger(__name__)


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
                body=f'Hello, {subscriber.username}! Here are the new articles in the category "{category.name}" for the past week.',
                from_email='erdes3182@yandex.ru',
                to=[subscriber.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_weekly_articles,
            trigger=CronTrigger(day_of_week="mon", hour=10, minute=0),
            id="send_weekly_articles",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'send_weekly_articles'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")