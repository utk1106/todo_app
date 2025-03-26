from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from base.models import Task
from datetime import timedelta

class Command(BaseCommand):
    help = 'Sends email reminders for tasks due soon'

    def handle(self, *args, **options):
        # Find tasks due within the next 10 minutes (updated logic)
        now = timezone.now()
        reminder_threshold_start = now
        reminder_threshold_end = now + timedelta(minutes=10)
        tasks_to_remind = Task.objects.filter(
            complete=False,
            reminded=False,
            due_date__isnull=False,
            due_date__gte=reminder_threshold_start,
            due_date__lte=reminder_threshold_end
        )
        
        self.stdout.write(f"Found {tasks_to_remind.count()} tasks that need reminders")
        
        # Group tasks by user for consolidated emails
        user_tasks = {}
        for task in tasks_to_remind:
            if task.user and task.user.email:
                if task.user.id not in user_tasks:
                    user_tasks[task.user.id] = {
                        'user': task.user,
                        'tasks': []
                    }
                user_tasks[task.user.id]['tasks'].append(task)
        
        # Send emails to each user
        for user_id, data in user_tasks.items():
            user = data['user']
            tasks = data['tasks']
            
            task_list = "\n".join([
                f"- {task.title} (Due: {task.due_date.strftime('%Y-%m-%d %H:%M')})"
                for task in tasks
            ])
            
            subject = "Reminder: You have tasks due soon"
            message = f"""Hello {user.username},

You have the following tasks due within the next 10 minutes:

{task_list}

Please log in to complete them: http://localhost:8000/

Thank you,
Your Todo App
"""
            
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS(f"Sent reminder email to {user.email}"))
                
                # Mark tasks as reminded
                for task in tasks:
                    task.reminded = True
                    task.save()
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to send email to {user.email}: {str(e)}"))
        
        self.stdout.write(self.style.SUCCESS('Reminder process completed'))



# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from base.models import Task  # Updated import to match your app name
# from django.core.mail import send_mail

# class Command(BaseCommand):
#     help = 'Sends reminders for upcoming tasks'

#     def handle(self, *args, **options):
#         now = timezone.now()
#         upcoming_tasks = Task.objects.filter(
#             due_date__lte=now + timezone.timedelta(hours=1),
#             due_date__gte=now,
#             reminded=False,
#             complete=False  # Only remind for incomplete tasks
#         )

#         for task in upcoming_tasks:
#             send_mail(
#                 f'Reminder: {task.title}',
#                 f'Your task "{task.title}" is due at {task.due_date}.',
#                 'from@example.com',  # Replace with your email
#                 [task.user.email],
#                 fail_silently=False,
#             )
#             task.reminded = True
#             task.save()
#             self.stdout.write(self.style.SUCCESS(f'Reminded {task.user.email} about {task.title}'))