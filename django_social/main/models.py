from django.db import models
from account.models import User
from datetime import datetime
from django.urls import reverse
import uuid
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.core.validators import FileExtensionValidator
from PIL import Image, ImageFilter
from django.core.files.base import ContentFile
from io import BytesIO


def user_directory_path(instance, filename):
    return 'posts/{0}/{1}/{2}'.format(instance.user.id, datetime.now().strftime('%Y-%m-%d'), filename)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=user_directory_path, null=True, 
                              validators= [
                                FileExtensionValidator (
                                    allowed_extensions=["jpg", "jpeg", "png", "webp"],
                                    message='{extention} is not allowed. allowed extensions arer  jpg, jpeg, png'
                                        )
                                    ]
                                )
    photo_standard = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(406, 227)],
        format='JPEG',
        options={"quality": 90}
    )
    created = models.DateTimeField(auto_now_add=True)  
    updated = models.DateTimeField(auto_now=True)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='post_like', blank=True)
    bookmarks = models.ManyToManyField(User, related_name='saved_posts', blank=True)
    tagged_users = models.ManyToManyField(User, related_name='tagged_posts', blank=True)

    title = models.CharField(max_length=250, blank=False)
    slug = models.SlugField(unique=True) 

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')

    def __str__(self):
        return f'Post by {self.user.username}'
    
    def get_absolute_url(self):
        return reverse('main:post_detail', args=[self.slug])

    @property
    def number_of_likes(self):
        return self.likes.count()
    
    @property
    def number_of_bookmarks(self):
        return self.bookmarks.count()
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        target_width = 1000
        img = Image.open(self.photo)
        target_height = img.height
        target_width = max(target_width, img.width)
        background = Image.new("RGB", (target_width, target_height))
        blurred_image = img.filter(ImageFilter.GaussianBlur(10))
        background.paste(blurred_image, ((target_width - img.width) // 2, 0))
        offset = ((target_width - img.width) // 2, 0) 
        background.paste(img, offset)

        buffer = BytesIO()
        background.save(buffer, format='JPEG')

        original_filename = self.photo.name.split('/')[-1]
        self.photo.save(original_filename, ContentFile(buffer.getvalue()), save=False)

        return super().save(*args, **kwargs)
    
    
class Like(models.Model):

    LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
        )
    
    post = models.ForeignKey(Post, verbose_name='liked_post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='liking_user', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    value = models.CharField(max_length=50, choices=LIKE_CHOICES)

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"
    
    def delete(self, *args, **kwargs):
        self.post.likes.remove(self.user)
        super().delete(*args, **kwargs)



class Bookmark(models.Model):

    LIKE_CHOICES = (
    ('Save', 'Save'),
    ('Unsave', 'Unsave'),
        )
    
    post = models.ForeignKey(Post, verbose_name='saved_post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='saving_user', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    value = models.CharField(max_length=50, choices=LIKE_CHOICES)

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"


    def delete(self, *args, **kwargs):
        self.post.bookmarks.remove(self.user)
        super().delete(*args, **kwargs)





class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_comment', blank=False, on_delete=models.CASCADE)
    content = models.CharField(max_length=350, blank=True, null=True)
    parent = models.ForeignKey("self", related_name='comment_reply',
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=
                                   True)
    
    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()
    
    def __str__(self):
        return f'{self.user}: {self.content[:25] if self.content else ""}'