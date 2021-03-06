import textwrap as tw

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )


class Group(models.Model):
    title = models.CharField(
        verbose_name='Заголовок', max_length=200,
        help_text='Напишите название группы'
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, related_name='group', blank=True,
        null=True, db_index=True
    )

    def __str__(self):
        return tw.fill(self.text, width=50), self.author


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
