from django.core.management.base import BaseCommand
from django.utils import timezone
from base.models import Task  # Updated import to match your app name
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Sends reminders for upcoming tasks'

    def handle(self, *args, **options):
        now = timezone.now()
        upcoming_tasks = Task.objects.filter(
            due_date__lte=now + timezone.timedelta(hours=1),
            due_date__gte=now,
            reminded=False,
            complete=False  # Only remind for incomplete tasks
        )

        for task in upcoming_tasks:
            send_mail(
                f'Reminder: {task.title}',
                f'Your task "{task.title}" is due at {task.due_date}.',
                'from@example.com',  # Replace with your email
                [task.user.email],
                fail_silently=False,
            )
            task.reminded = True
            task.save()
            self.stdout.write(self.style.SUCCESS(f'Reminded {task.user.email} about {task.title}'))