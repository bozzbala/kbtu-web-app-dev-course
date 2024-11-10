from django.db import models

class PublishedPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

    def by_author(self, author_name):
        return self.get_queryset().filter(author=author_name)

class Category(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
    is_published = models.BooleanField(default=True)

    objects = models.Manager()
    published = PublishedPostManager()

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

class Comment(models.Model):
    comment = models.TextField()
    post = models.OneToOneField(
        Post,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.post.title