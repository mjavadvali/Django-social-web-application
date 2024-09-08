from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    # path('', views.dashboard, name='dashboard'),
    # path('register/', views.register, name='register'),
    # path('edit/', views.edit, name='edit'),
    path('login/', views.Login.as_view(redirect_authenticated_user=True), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard', views.UserDashboardView.as_view(), name='dashboard'),
    path('dashboard/saved', views.saved_posts, name='saved'),
    path('dashboard/personal_info', views.personal_info, name='personal_information'),
    path('dashboard/user_settings', views.user_settings, name='user_settings'),
    path('profile/<str:username>', views.UserProfileView.as_view(), name='profile'),
    path('profile/profile_settings', views.profile_settings, name='profile_settings'),
    # path('follow_user/<str:username>', views.follow_user, name='follow_user'),       
]