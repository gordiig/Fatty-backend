from django.core import management
from huey import crontab
from huey.contrib.djhuey import db_periodic_task


@db_periodic_task(crontab(day_of_week='6', hour='18'))
def backup_on_saturday():
    """
    Делает бэкап БД и медиа каждую субботу в 18:00
    """
    management.call_command('dbbackup', clean=True)
    management.call_command('mediabackup', clean=True)
