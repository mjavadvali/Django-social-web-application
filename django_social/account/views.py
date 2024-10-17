from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import User, UserFollowing
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import Post, Bookmark
from django.core.files.storage import FileSystemStorage




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
        return get_object_or_404(User, username=self.kwargs['username'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()  

        followings = UserFollowing.objects.filter(following_user=user)
        context['followings'] = [relation.followed_user for relation in followings]
        
        followers = UserFollowing.objects.filter(followed_user=user)
        context['followers'] = [relation.following_user for relation in followers]
        
        is_following = UserFollowing.objects.filter(following_user=self.request.user, followed_user=user, value='Follow').exists()
        context['is_following'] = is_following
        
        context['user_posts'] = Post.objects.filter(user=user)
        context['user'] = user
        
        return context
    
    def post(self, request, username, *args, **kwargs):
        following_user = request.user  
        followed_user = get_object_or_404(User, username=username)  
        follow_relation = UserFollowing.objects.filter(following_user=following_user, followed_user=followed_user).first()



        if follow_relation:
            if follow_relation.value == 'Follow':
                print('follow_relation.value == Follow')
                follow_relation.value = 'Unfollow'
                following_user.followings -= 1
                followed_user.followers -= 1
            else:
                print('follow_relation.value == else')
                follow_relation.value = 'Follow'
                following_user.followings += 1
                followed_user.followers += 1
            follow_relation.save()
        else:
            print('if not follow_relation')
            UserFollowing.objects.create(following_user=following_user, followed_user=followed_user, value='Follow')
            following_user.followings += 1
            followed_user.followers += 1
        
        following_user.save()
        followed_user.save()
    

        return redirect(reverse('profile', args=[username]))
       

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
    
    def post(self, request, *args, **kwargs):
        print('herer is toggled')
        uploaded_file = request.FILES['avatar']  
        fs = FileSystemStorage()  
        filename = fs.save(uploaded_file.name, uploaded_file)  

        user = get_object_or_404(User, pk=self.request.user.pk) 
        user.profile_img = filename
        user.save()
      
        return redirect(reverse('dashboard'))


def show_followings(request, username):
    user = get_object_or_404(User, username=username)
    followings = UserFollowing.objects.filter(following_user=user, value='Follow')

    following_users = [following.followed_user for following in followings]

    return render(request, 'account/profile/followings.html', {'followings': following_users})


def show_followers(request, username):
    user = get_object_or_404(User, username=username)
    followers = UserFollowing.objects.filter(followed_user=user, value='Follow')

    follower_users = [follower.followed_user for follower in followers]

    return render(request, 'account/profile/followers.html', {'followers': follower_users})



def profile_settings(request):
    pass

    
def saved_posts(request):
    saved_posts = Bookmark.objects.filter(user= request.user)
    return render(request, 'account/dashboard/saved_posts.html', {'saved_posts': saved_posts})

def personal_info(request):
    return render(request, 'account/dashboard/information.html')


def user_settings(request):
    return render(request, 'account/dashboard/settings.html')


