from django.db import models
from config.settings import AUTH_USER_MODEL
from products.models import Product


class Style(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return str(self.name)


class Article(models.Model):
    author = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles"
    )
    title = models.CharField(max_length=128)
    content = models.TextField()
    likes = models.ManyToManyField(
        AUTH_USER_MODEL, related_name="article_likes", blank=True
    )
    image = models.ImageField(upload_to="article_pics", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    styles = models.ManyToManyField(Style, related_name="articles")
    products = models.ManyToManyField(Product, related_name="articles", blank=True)

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        AUTH_USER_MODEL, related_name="comment_likes", blank=True
    )

    def __str__(self):
        return str(self.content)
