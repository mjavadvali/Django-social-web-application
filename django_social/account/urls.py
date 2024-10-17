from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

# app_name = 'account'

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
    path('profile/<str:username>/followings', views.FollowingsListView.as_view(), name='followings'),
    path('profile/<str:username>/followings', views.FollowingsListView.as_view(), name='followings_follow'),
    path('profile/<str:username>/followers', views.FollowersListView.as_view(), name='followers'),

    # path('follow_user/<str:username>', views.follow_user, name='follow_user'),       
    # path('follow_user/<uuid:id>', views.follow_user, name='follow_user'),


    # path('profile/<str:username>/followings/', UserFollowListView.as_view(), {'follow_type': 'followings'}, name='user-followings'),
    # # URL for viewing followers
    # path('profile/<str:username>/followers/', UserFollowListView.as_view(), {'follow_type': 'followers'}, name='user-followers'),
]