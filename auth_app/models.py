from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, **extra_fields):
        """
            creates and saves the user with given email and password
        """
        if not email:
            raise ValueError('User must have an email address. ')

        if not password:
            raise ValueError("Users must have a password.")

        if not first_name:
            raise ValueError("Users must have a first_name")

        if not last_name:
            raise ValueError("Users must have a last_name")

        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name, password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email,first_name, last_name, password, **extra_fields):
        user = self.create_user(email,first_name=first_name, last_name=last_name, password=password, **extra_fields)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        user = self.create_user(email, first_name=first_name, last_name=last_name, password=password, **extra_fields)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class Education(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(AbstractBaseUser, PermissionsMixin):
    LOGIN_TYPES = [
        (1, 'Manual'),
        (2, 'Linkedin'),
        (3, 'Google')
    ]
    TITLES = [
        ('Dr', 'Dr'),
        ('Miss', 'Miss'),
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Ms', 'Ms'),
        ('Mx', 'Mx'),
        ('Prof', 'Prof'),
    ]
    title = models.CharField(max_length=6, choices=TITLES, default='', null=True, blank=True)
    first_name = models.CharField(max_length=255, blank=False, null=False, default='')
    last_name = models.CharField(max_length=255, blank=False, null=False, default='')
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    password = models.CharField(max_length=32, null=False, blank=False)
    phone_number = models.CharField(max_length=12, blank=True, null=True, default='')
    profile_pic = models.ImageField(default='', upload_to='ProfileImages', blank=True, null=True)
    education = models.ForeignKey(Education, on_delete=models.CASCADE, default=1)
    language = models.ManyToManyField(Language, default=1)
    bool_driving_licence = models.BooleanField(default=False)
    bool_own_vehicle = models.BooleanField(default=False)
    isPaidUser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    login_type = models.CharField(default=1, blank=True, null=True, max_length=30, choices=LOGIN_TYPES)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        # user is identified by their email address
        return self.first_name +' '+self.last_name

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user is member of staff?"
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def education_name(self):
        return self.education.name

    @property
    def language_name(self):
        return [i.name for i in self.language.all()]

    # @property
    # def is_active(self):
    #     return self.is_active

    @staticmethod
    def all_users():
        qs = User.objects.values_list('email', flat=True)
        return qs

    objects = UserManager()

# class Shortnig(models.Model):
#     url = models.URLField()
#     short_url = models.SlugField(max_length = 250, null=True, blank=True)