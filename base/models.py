from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

# Remove this import since we're not using the default User model
# from django.contrib.auth.models import User
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError(_('The Phone Number must be set'))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(phone_number, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)  # e.g., +1234567890
    username = models.CharField(max_length=150, unique=True)     # For display purposes
    email = models.EmailField(unique=True, blank=False, null=False)  # Make required
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Specify unique related_name for groups and user_permissions to avoid clash
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Unique related_name
        blank=True,
        help_text=_('The groups this user belongs to.'),
        verbose_name=_('groups'),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # Unique related_name
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions'),
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'  # Use phone_number for authentication
    REQUIRED_FIELDS = ['username']   # Required when creating a superuser

    def __str__(self):
        return self.phone_number

# Create your models here.
class Task(models.Model):
    # Update to use CustomUser instead of User
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True) #added for cron job
    reminded = models.BooleanField(default=False)  # Added for cron job
    popup_reminder = models.BooleanField(default=False)  # New field for popup

    #after adding due_date and reminded and running python3 manage.py makemigrations, migration folder added new field
    # and after than running python3 manage.py migrate, the new field was added to the database sql3

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['complete', 'due_date']
