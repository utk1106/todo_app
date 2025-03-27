# Django To-Do List with Popup Reminders

## Overview
A simple Django-based to-do list application with email and popup reminders for tasks due within 10 minutes. Built with Django, Bootstrap, and cron jobs for automated reminders.

## Features
- **Task Management:** Add, edit, view, and delete tasks with due dates.
- **Email Reminders:** Sends email reminders for tasks due within 10 minutes (logged to console with `console.EmailBackend`).
- **Popup Reminders:** Displays a popup on the `/tasks/` page for tasks due within 10 minutes.
- **Cron Jobs:** Automates reminders using `send_reminders` and `mark_popup_reminders` management commands.

## Project Structure
### Base App (`base/`):
- `models.py`: Defines `Task` and `CustomUser` models.
- `views.py`: Handles task CRUD operations.
- `templates/base/task_list.html`: Renders the task list with a popup reminder.
- `management/commands/send_reminders.py`: Sends email reminders.
- `management/commands/mark_popup_reminders.py`: Marks tasks for popup reminders.

### Settings (`todo_list/settings.py`):
- Configures Django settings, including `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`.

## Setup Instructions

### Prerequisites
- Python 3.9+
- Virtual environment (`myenv`)
- Cron (for scheduling reminders)

### Installation
1. **Clone the Repository:**
   ```sh
   git clone <repository-url>
   cd todo_list
   ```

2. **Set Up Virtual Environment:**
   ```sh
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run Migrations:**
   ```sh
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

5. **Create a Superuser:**
   ```sh
   python3 manage.py createsuperuser
   ```

6. **Run the Development Server:**
   ```sh
   python3 manage.py runserver
   ```

## Configure Cron Jobs
The app uses cron jobs to send email reminders and mark tasks for popup reminders every 10 minutes.

### Edit Crontab:
```sh
crontab -e
```

### Add the following lines:
```sh
# Run Django management commands every 10 minutes
*/10 * * * * /bin/bash -c "export DJANGO_SETTINGS_MODULE=todo_list.settings && cd /home/utkarsh/todo_list && /home/utkarsh/todo_list/myenv/bin/python3 /home/utkarsh/todo_list/manage.py send_reminders >> /home/utkarsh/todo_list/cron.log 2>&1"

*/10 * * * * /bin/bash -c "export DJANGO_SETTINGS_MODULE=todo_list.settings && cd /home/utkarsh/todo_list && /home/utkarsh/todo_list/myenv/bin/python3 /home/utkarsh/todo_list/manage.py mark_popup_reminders >> /home/utkarsh/todo_list/cron.log 2>&1"
```

### Ensure Cron Is Running:
```sh
sudo systemctl status cron
sudo systemctl start cron
sudo systemctl enable cron
```

## Usage
### Access the App:
Go to `http://localhost:8000/tasks/` and log in (e.g., as `testuser2`).

### Create a Task:
Add a task with a due date (e.g., 5 minutes from now):
```sh
python3 manage.py shell
```
```python
from base.models import Task, CustomUser
from django.utils import timezone

user = CustomUser.objects.get(username='testuser2')
Task.objects.create(
    user=user,
    title="Popup Test for Testuser2",
    due_date=timezone.now() + timezone.timedelta(minutes=5)
)
exit()
```

### Wait for Reminders:
- **Email Reminder:** Sent when the task is due within 10 minutes (logged to console).
- **Popup Reminder:** Appears on the `/tasks/` page when the task is due within 10 minutes.

## Popup Reminder Feature
- **Appearance:** A red popup in the top-right corner of the `/tasks/` page.
- **Message:** `Task "Popup Test for Testuser2" is due in 4 minutes!`.
- **Dismiss Button:** Click "Dismiss" to hide the popup.

## Troubleshooting
### Cron Jobs Not Running:
- Check the cron log: `cat /home/utkarsh/todo_list/cron.log`.
- Verify cron service: `sudo systemctl status cron`.
- Ensure paths in crontab match your setup.

### Popup Not Appearing:
- Ensure `mark_popup_reminders` has run.
- Check browser console (F12) for JavaScript errors.

### Email Not Sending:
- Verify `EMAIL_BACKEND` in `settings.py`.
- Check console for email logs.

---
Now you're all set to use the Django To-Do List with popup reminders! 🚀
