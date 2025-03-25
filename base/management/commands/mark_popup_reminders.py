from django.core.management.base import BaseCommand
from django.utils import timezone
from base.models import Task
from datetime import timedelta

class Command(BaseCommand):
    help = 'Marks tasks due in 10 minutes for popup reminders'

    def handle(self, *args, **options):
        now = timezone.now()
        reminder_threshold = now + timedelta(minutes=10)
        tasks_to_mark = Task.objects.filter(
            complete=False,
            popup_reminder=False,  # Only unmarked tasks
            due_date__isnull=False,
            due_date__lte=reminder_threshold,
            due_date__gte=now
        )

        count = tasks_to_mark.count()
        self.stdout.write(f"Found {count} tasks for popup reminders")

        if count > 0:
            for task in tasks_to_mark:
                task.popup_reminder = True
                task.save()
                self.stdout.write(f"Marked task '{task.title}' for popup (Due: {task.due_date})")

        self.stdout.write(self.style.SUCCESS('Popup reminder marking completed'))