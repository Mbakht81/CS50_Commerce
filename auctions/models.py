from dataclasses import dataclass
from datetime import datetime
from unicodedata import category
from venv import create
from django.contrib.auth.models import AbstractUser
from django.db import models



class Category(models.Model):
    name =models.CharField(max_length=64)
    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=130)
    image_url = models.CharField(max_length=64, blank=True)
    amount = models.IntegerField (default=0)
    category = models.ForeignKey(Category, default=0 , blank=True , on_delete= models.PROTECT, related_name="listings")
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=datetime.now, blank=True)
    created_by  = models.ForeignKey('User', default= None, on_delete=models.CASCADE, related_name="listings")
    
    def __str__(self):
        return self.title +self.description


class User(AbstractUser):
    watchlist = models.ManyToManyField(Listing, blank=True, related_name="prospects")
    def __str__(self):
        return self.username





class Bid(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount  = models.IntegerField(default=0)
    created_date   =models.DateTimeField(default = datetime.now)
    def __str__(self):
        return f"{self.user} on {self.listing} : ${self.amount} "



class Comment(models.Model):
    user  = models.ForeignKey(User,on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=255)
    created_date = models.DateTimeField(default=datetime.now)


