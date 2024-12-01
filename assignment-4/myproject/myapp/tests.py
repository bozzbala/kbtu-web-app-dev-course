from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Post, Comment
from django.contrib.auth.models import User

class PostAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        self.post = Post.objects.create(
            title='Post 1',
            content='Content 1',
            author='testuser',
            published_date='2024-01-01T00:00:00Z',
            image=None
        )
        self.post.save()

    def test_list_posts(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_post(self):
        data = {
            'title': 'Post 2',
            'content': 'Content 2',
            'author': 'testuser',
            'published_date': '2024-01-02T00:00:00Z',
            'image': None
        }
        response = self.client.post(reverse('post-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_retrieve_post(self):
        response = self.client.get(reverse('post-detail', args=[self.post.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Post 1')

    def test_update_post(self):
        data = {
            'title': 'Post 1 Updated',
            'content': 'Content 1 Updated',
            'author': 'testuser',
            'published_date': '2024-01-01T00:00:00Z',
            'image': None
        }
        response = self.client.put(reverse('post-detail', args=[self.post.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Post 1 Updated')

    def test_delete_post(self):
        response = self.client.delete(reverse('post-detail', args=[self.post.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_list_comments_for_post(self):
        comment = Comment.objects.create(post=self.post, content='Comment 1')
        response = self.client.get(reverse('comment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_comment_for_post(self):
        data = {
            'post': self.post.id,
            'content': 'Comment 2'
        }
        response = self.client.post(reverse('comment-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
