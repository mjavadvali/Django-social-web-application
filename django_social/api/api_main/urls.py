from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'posts', views.PostViewSet, basename='posts')

urlpatterns = [
    path("", include(router.urls)),
    path("create_post/",views.PostCreate.as_view() ),
    path('post_list/', views.post_list),
    path('posts/post_detail/<uuid:pk>', views.PostDetailView.as_view(), name='api_delete_post')
]
