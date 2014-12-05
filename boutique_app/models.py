from django.db import models

# Create your models here.
class Users(models.Model):
    LoginName = models.CharField(max_length=256)
    Password  = models.CharField(max_length=256)

class Products(models.Model):
    ProductID   = models.PositiveIntegerField()
    Heading     = models.CharField(max_length=256)
    Description = models.CharField(max_length=1024)
    Price       = models.CharField(max_length=20)

class ProductImages(models.Model):
    ProductFK   = models.ForeignKey(Products)
    ImageID   = models.PositiveIntegerField()
    ImageName   = models.CharField(max_length=256)
    ThumbNail   = models.CharField(max_length=256)

