from django.shortcuts import render, get_object_or_404
from .models import User
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import Post, Bookmark
from django.http import JsonResponse




class Login(SuccessMessageMixin, LoginView):
    template_name= 'account/registration/login.html'
    success_url = reverse_lazy('')
    success_message = f'Dear , you have logged in the website successfully.'


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'account/registration/signup.html'
    model = User
    success_url = reverse_lazy('main:listview')
    form_class = SignUpForm
    success_message = f'Dear ..., you have been signned up successfully.'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        authenticate(user)
        login(self.request, user)
        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'account/profile/profile.html'
    
    def get_object(self):
        return self.kwargs['username']
    
    def get_context_data(self, **kwargs):
        print('request is', self.kwargs['username'])
        user = get_object_or_404(User, username=self.kwargs['username'])
        is_following = user in self.request.user.follows.all() if self.request.user.is_authenticated else False

        context = super().get_context_data(**kwargs)
        context['is_following'] = is_following
        context['user_posts'] = Post.objects.filter(user=user)
        context['user'] = user
        return context
    
    def post(self, request, username, *args, **kwargs):
        you = request.user
        following_users = you.follows.all()
        user = get_object_or_404(User, username=username)
        
        if user in following_users:
            is_following = True
        else:
            is_following = False

        if request.method == 'POST':
            if is_following:
                you.follows.remove(user)
                you.followings -= 1
                you.save()
                is_following = False
            else:
                you.follows.add(user)
                you.followings += 1
                you.save()
                is_following = True
        return JsonResponse({"is_following": is_following})
                
    

class UserDashboardView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'account/dashboard/dashboard.html'
    context_object_name = 'user'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['user_posts'] = Post.objects.filter(user=self.request.user)
        print(f"User: {self.request.user}, Posts: {context['user_posts']}")  
        return context

def profile_settings(request):
    pass

    
def saved_posts(request):
    saved_posts = Bookmark.objects.filter(user= request.user)
    return render(request, 'account/dashboard/saved_posts.html', {'saved_posts': saved_posts})

def personal_info(request):
    return render(request, 'account/dashboard/information.html')


def user_settings(request):
    return render(request, 'account/dashboard/settings.html')



