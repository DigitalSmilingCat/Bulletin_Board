from datetime import datetime, timedelta
from .tasks import scheduler
from .models import CheckCode
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=CheckCode)
def delete_check_code(sender, instance, **kwargs):
    # Создаем задачу для удаления объекта CheckCode через 3 минуты
    delete_time = datetime.now() + timedelta(minutes=3)
    code_id = instance.id
    scheduler.add_job(
        delete_check_code_task,
        "date",
        run_date=delete_time,
        args=[code_id],
        id=f"delete_check_code_{code_id}",
    )


def delete_check_code_task(code_id):
    CheckCode.objects.filter(id=code_id).delete()


scheduler.start()