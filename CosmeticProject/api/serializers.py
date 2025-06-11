from rest_framework import serializers
from .models import Blog , Blog_position
from drf_extra_fields.fields import Base64ImageField

class BlogSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    class Meta:
        model = Blog
        fields = '__all__'

class Blog_positionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog_position
        fields = '__all__'
