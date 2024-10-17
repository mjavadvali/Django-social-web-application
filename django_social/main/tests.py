from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
from main.models import Post, User
import tempfile

class PostModelTest(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='12345', email='test@gmail.com')
    
    def create_test_image(self, image_format='JPEG'):
        # Create a simple image for testing
        img = Image.new('RGB', (100, 100), color = (73, 109, 137))
        buffer = BytesIO()
        img.save(buffer, format=image_format)
        buffer.seek(0)
        return SimpleUploadedFile(r"C:\Users\ali\Desktop\black tea.jpeg", buffer.read(), content_type="image/jpeg")
    
    def test_post_photo_save_and_processing(self):
        # Create a post with an image
        test_image = self.create_test_image()
        post = Post.objects.create(
            user=self.user,
            title="Test Post",
            content="Test Content",
            photo=test_image,
            status="published"
        )

        # Check if the post is created and the photo field is not empty
        self.assertIsNotNone(post.photo)
        
        # Re-fetch the post from the database
        post.refresh_from_db()

        # Check if the slug is generated correctly
        self.assertEqual(post.slug, "test-post")

        # Check if the image has been processed (blurred and resized)
        img = Image.open(post.photo.path)
        self.assertEqual(img.width, 100)  # Width should be the same as before
        self.assertEqual(img.height, 100)  # Height should be the same as before
