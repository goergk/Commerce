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

    def __str__(self):
        f"{self.name}"

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=2500)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image_url = models.CharField(max_length=500)
    creation_date = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField()
    creator =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_creator")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_categories")
    
    def __str__(self):
        f"{self.title} by {self.creator}"

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidders")
    bid = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        f"Last bid: {self.date} by {self.user}. Bid value: {self.value}$."

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=64)
    content = models.CharField(max_length=2500)
    date = models.DateTimeField()
    commentator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="original_poster")
    comment = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        f"{self.topic}: \n{self.content}"



