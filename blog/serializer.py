from rest_framework import serializers
from .models import Posts


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        models = Posts
        fields = ['title', 'content']
        # fields = '__all__'
