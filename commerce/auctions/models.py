from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.expressions import Value


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass

    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    image_url = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f'{self.name}'

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=2500)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image_url = models.CharField(max_length=500, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField(null=True, blank=True)
    closed = models.BooleanField(default=False)
    creator =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_creator")
    winner =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_winner", blank=True, null=True)
    follower = models.ManyToManyField(User, related_name="watchlist_listings", blank=True)
    category = models.ManyToManyField(Category, related_name="listings", blank=True)
    
    def __str__(self):
        return f"{self.title} by {self.creator}"

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidders")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"Last bid: {self.value}$ by {self.user}."

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=64)
    content = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    commentator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentators")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.topic}: \n{self.content}"



