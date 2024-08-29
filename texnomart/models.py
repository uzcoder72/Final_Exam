from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    primary_image = models.ImageField(upload_to='products/')
    is_liked = models.BooleanField(default=False)  # Keep this for some other purpose if needed

    def __str__(self):
        return self.name

class AttributeKey(models.Model):
    name = models.CharField(max_length=255)

class AttributeValue(models.Model):
    key = models.ForeignKey(AttributeKey, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    product = models.ForeignKey(Product, related_name='attributes', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.key.name}: {self.value}"

class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

class Image(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    url = models.ImageField(upload_to='products/images/')
