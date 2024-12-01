from django.db import models

class PostManager(models.Manager):
    def get_published_posts(self):
        return self.filter(published_date__isnull=False)
    
    def get_posts_from_author(self, author):
        return self.filter(author=author)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=70)
    published_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)

    objects = PostManager()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.post.__str__() + " comment"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
