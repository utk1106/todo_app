from django.db import migrations, models

def set_valid_emails(apps, schema_editor):
    CustomUser = apps.get_model('base', 'CustomUser')
    users = CustomUser.objects.filter(email__isnull=True)
    if not users.exists():
        print("No users with NULL emails found.")
        return
    print(f"\nFound {users.count()} users with no email. Please provide valid emails:")
    for user in users:
        while True:
            email = input(f"Enter email for user {user.phone_number} (username: {user.username}): ")
            if email and '@' in email:  # Basic validation
                try:
                    user.email = email
                    user.save()
                    print(f"Set email for {user.phone_number} to {email}")
                    break
                except Exception as e:
                    print(f"Error: {e}. Try a different email (must be unique).")
            else:
                print("Invalid email format. Please include '@'.")

def reverse_set_valid_emails(apps, schema_editor):
    CustomUser = apps.get_model('base', 'CustomUser')
    CustomUser.objects.all().update(email=None)

class Migration(migrations.Migration):
    dependencies = [
        ('base', '0001_initial'),  # Adjust if your last migration differs
    ]
    operations = [
        migrations.RunPython(set_valid_emails, reverse_code=reverse_set_valid_emails),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(unique=True, blank=False, null=False),
        ),
    ]