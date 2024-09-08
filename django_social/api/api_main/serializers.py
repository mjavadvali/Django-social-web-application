from rest_framework import serializers
from main.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'photo', 'pk']
        read_only_fields = ['user', ]
    
