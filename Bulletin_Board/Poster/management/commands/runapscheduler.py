import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.utils.timezone import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import timedelta
from Poster.models import Poster, User


logger = logging.getLogger(__name__)


def weekly_email_job():
    start_date = datetime.today() - timedelta(days=7)
    weekly_posters = Poster.objects.filter(created__gt=start_date)
    if weekly_posters:
        all_users = User.objects.all()
        recipients = []
        for user in all_users:
            recipients.append(user.email)
        html_content = render_to_string(
            'weekly_email.html', {
                'poster_list': weekly_posters.values('pk', 'title'),
                'domain': '127.0.0.1',
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'Посты за прошедшую неделю',
            body="poster_list",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipients
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            weekly_email_job,
            trigger=CronTrigger(week="*"),
            # trigger=CronTrigger(second="*/10"),
            id="weekly_email_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_email_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")