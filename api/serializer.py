from users.models import Post
from rest_framework.serializers import ModelSerializer

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['user_name', 'post_title', 'post_content', 'date_published', 'user_profile_link']