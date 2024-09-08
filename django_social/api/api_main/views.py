from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import PostSerializer
from main.models import Post
from django.core.exceptions import PermissionDenied

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostCreate(ListCreateAPIView):
        queryset = Post.objects.all()
        serializer_class = PostSerializer

        def perform_create(self, serializer):
            serializer.save(user=self.request.user)

class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_update(self, serializer):
        # Optional: Customize behavior when updating
        serializer.save(user=self.request.user)  # Ensure the current user is retained

    def perform_destroy(self, instance):
        # Optional: Customize behavior before deleting a post
        # For example, check if the request user is the owner of the post
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this post.")
        instance.delete()

     

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from main.models import Post
from api.api_main.serializers import PostSerializer


@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
