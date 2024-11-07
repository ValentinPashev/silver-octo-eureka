
from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(
        max_length=200
    )

    text = models.TextField(

    )

    created_date = models.DateTimeField(
        auto_now_add=True,

    )

    created_by = models.CharField(
        max_length=30
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    author = models.CharField(
        max_length=100,
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )