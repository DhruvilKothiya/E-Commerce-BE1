from django.db import models
from django.contrib.auth.models import AbstractUser

# Create User table
class User(AbstractUser):
    class Role(models.TextChoices): 
        ADMIN = "ADMIN", "Admin"
        CUSTOMER = "CUSTOMER", "Customer"

    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        default=Role.ADMIN
    )

    def save(self, *args, **kwargs):
        if not self.pk and not self.role: 
            self.role = self.Role.ADMIN  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

# Create Categories model
class Categories(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Create Products model
class Products(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    productname = models.CharField(max_length=100)
    productinfo = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True) 
    createdAt = models.DateTimeField(auto_now_add=True)
    stockcount = models.IntegerField(null=True, blank=True, default=0)
    productbrand = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True,default=0  )
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True ,default="a")

    def __str__(self):
        return self.productname 

# Create Wishlist model
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.productname}"
