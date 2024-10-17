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
    posts = models.IntegerField(default=0)
    followings = models.PositiveIntegerField(default=0)
    followers = models.PositiveIntegerField(default=0)
    objects = CustomUserManager()

    REQUIRED_FIELDS = ['email', ]


    def get_absolute_url(self):
        return reverse('profile', args=[self.username])

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class UserFollowing(models.Model):

    FOLLOW_CHOICES = (
        ('Follow', 'Follow'),
        ('Unfollow', 'Unfollow'),
    )
    
    following_user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, related_name='followed_by', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    value = models.CharField(max_length=50, choices=FOLLOW_CHOICES)


    def __str__(self):
        return f'{self.following_user} follows {self.followed_user}'
    

    # def save(self, *args, **kwargs):
    #     following_user = User.objects.get(username=self.following_user.username)
    #     followed_by = User.objects.get(username=self.followed_user.username)
        
    #     if self.value == 'Follow': 
    #         following_user.followings += 1
    #         following_user.save()
    #         followed_by.followings += 1
    #         followed_by.save()
    #     elif self.value == 'Unfollow':       
    #         following_user.followings -= 1
    #         following_user.save()
    #         followed_by.followings -= 1
    #         followed_by.save()
    #     super().save(*args, **kwargs)
