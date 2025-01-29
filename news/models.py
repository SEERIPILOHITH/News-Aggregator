from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    topics = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

    def get_topics_list(self):
        # Helper function to return a list of topics
        return [topic.strip() for topic in self.topics.split(',')]

    def set_topics_list(self, topics):
        # Helper function to save the topics as a comma-separated string
        self.topics = ', '.join(topics)

class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    published_at = models.DateTimeField()
    url = models.URLField()

    def __str__(self):
        return self.title
    
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}, {self.article.title}"
