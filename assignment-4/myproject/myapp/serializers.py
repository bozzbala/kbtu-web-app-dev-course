from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'post', 'content']

class PostSerializer(serializers.ModelSerializer): 
    comments = CommentSerializer(many=True, read_only=True, source='comment_set')
    
    class Meta: 
        model = Post 
        fields = ['id', 'title', 'content', 'author', 'published_date', 'image', 'comments'] 
    
    def create(self, validated_data): 
        post = Post.objects.create(**validated_data) 
        return post 
        
    def update(self, instance, validated_data): 
        image = validated_data.get('image')
        instance.title = validated_data.get('title', instance.title) 
        instance.content = validated_data.get('content', instance.content) 
        instance.author = validated_data.get('author', instance.author) 
        instance.published_date = validated_data.get('published_date', instance.published_date) 
        instance.image = validated_data.get('image', instance.image) 
        
        instance.save() 
        return instance