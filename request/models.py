from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime
from django.utils import timezone
today = timezone.now
class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    last_name = None
    first_name = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'),max_length=14,blank=True)
    token = models.TextField(_('forget password token'),blank=True)
    name = models.CharField(_('user name'),blank=True,max_length=100)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

class TempUser(models.Model):
    """
    temporary model for registered email verification
    """
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'),max_length=14,blank=True)
    token = models.TextField(_('verification token'),blank=True)
    name = models.CharField(_('user name'),blank=True,max_length=100)
    password = models.CharField(_('password'),max_length=100)
 

class Donor(models.Model):
    donorid = models.BigAutoField(primary_key=True)
    email = models.ForeignKey(
        CustomUser, to_field='email', on_delete=models.CASCADE)
    name = models.CharField(blank=True,max_length=100)
    blood = models.CharField(max_length=10,default=None)
    age = models.IntegerField(default=None)
    phone = models.CharField(max_length=14,blank=True)
    city = models.CharField(max_length=50,default=None)
    district = models.CharField(max_length=50,default=None)
    state = models.CharField(max_length=50,default=None)
    country = models.CharField(max_length=50,default=None)
    pincode = models.CharField(max_length=6,default=None)
    #rollno = models.CharField(default=None,max_length=10)
    #instituition = models.CharField(max_length=50,default=None)
    available = models.BooleanField(default=True)
    eligible_date = models.DateTimeField(_('Next eligibility date '),default=datetime.datetime.now())
