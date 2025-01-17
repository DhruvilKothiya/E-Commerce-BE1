
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create User table

class User(AbstractUser):
    # Override the username field to be optional
    username = models.CharField(max_length=100, blank=True, null=True, unique=True)

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CUSTOMER = "CUSTOMER", "Customer"

    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        default=Role.ADMIN
    )

    # Override the save method to use email as the identifier
    def save(self, *args, **kwargs):
        if not self.pk and not self.username: 
            self.username = self.email  # Set email as username if not specified
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email 

# Create Categories model
class Categories(models.Model):
    # Define the available category options
    CATEGORY_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('shoes', 'Shoes'),
        ('bags', 'Bags'),
        ('kids', 'Kids'),
        ('clothing', 'Clothing'),
    ]
    
    # Use the choices parameter in the CharField    
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Create Products model
class Products(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    productname = models.CharField(max_length=100)
    productinfo = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    rating = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True) 
    numReviews=models.IntegerField(null=True, blank=True,default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    stockcount = models.IntegerField(null=True, blank=True, default=0)
    productbrand = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True )
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True )

    def __str__(self):
        return self.productname 

# Create Wishlist model
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.productname}"

#Create Multiple Image model
class Images(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f"Image for {self.product.productname}"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart for {self.user.username}"
    
class CartItem(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.productname}"

