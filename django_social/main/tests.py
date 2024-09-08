from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.forms.models import model_to_dict
from account.models import User
from .models import Post
from .forms import PostForm
from .views import PostCreateView

class PostCreateViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password', email='admin@gmail.com')
        self.client.login(username='testuser', password='password')
         
    def test_login_required(self):
        response = self.client.get(reverse('main:post_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
        self.assertContains(response, 'name="title"')

    def test_form_rendering(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/create_post.html')
        self.assertIsInstance(response.context['form'], PostForm)

    def test_form_submission_valid(self):
        form_data = {
            'title': 'Test Post Title',
            'content': 'Test Post Content'
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertTrue(Post.objects.filter(title='Test Post Title').exists())

    def test_form_submission_invalid(self):
        form_data = {
            'title': '',  # Invalid data
            'content': ''
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)  # Should return to form page
        self.assertFormError(response, 'form', 'title', 'This field is required.')
        self.assertFormError(response, 'form', 'content', 'This field is required.')

    def test_redirect_on_success(self):
        form_data = {
            'title': 'Valid Title',
            'content': 'Valid Content'
        }
        response = self.client.post(self.url, form_data)
        self.assertRedirects(response, reverse('main:listview'))  # Ensure redirection to the success URL

    def test_get_form_method(self):
        view = PostCreateView()
        form = view.get_form(PostForm)
        self.assertIsInstance(form, PostForm)