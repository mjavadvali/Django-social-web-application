from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.urls import reverse
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username.strip(), email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, )
    username = models.CharField(max_length = 50, blank = False, null = False, unique = True)  
    email = models.EmailField( max_length=50, unique=True)
    is_email_verified = models.BooleanField(default=False)
    first_name = models.CharField(default = "null", max_length=500, blank=False, null=False)
    last_name = models.CharField(default = "null", max_length=500, blank=False, null=False)
    is_staff = models.BooleanField(default=False, verbose_name='staff')
    bio = models.TextField(blank=True, max_length=500)
    profile_img = models.ImageField(upload_to='profile_images',default='/profile_images/avatar.png')
    followers = models.IntegerField(default=0)
    followings= models.IntegerField(default=0)
    posts = models.IntegerField(default=0)
    
    follows = models.ManyToManyField('self', related_name='followed_by', blank= True, symmetrical=False)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['email', ]


    def get_absolute_url(self):
        return reverse('profile', args=[self.username])

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)