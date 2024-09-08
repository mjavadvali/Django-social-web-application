
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
   path('', views.ListPost.as_view(), name='listview'),
   path('post_detail/<uuid:pk>', views.PostDetail.as_view(), name='post_detail'),
   path('handle_like/<uuid:post_id>', views.handle_like, name='handle_like'),
   path('search', views.search_view, name='search'),
   path('create_post', views.PostCreateView.as_view(), name='create_post'),
   path('handle_comment/<uuid:post_id>', views.handle_comment, name='handle_comment'),
   path('handle_comment/<uuid:post_id>/<int:parent_id>', views.handle_comment, name='handle_parent_comment'),
   path('delete_post/<uuid:post_id>', views.post_delete, name='post_delete'),
   path('bookmark/<uuid:post_id>', views.bookmark_post, name='bookmark_post'),
   path('create_post/tag_users', views.tag_users, name='tag_users'),


]


