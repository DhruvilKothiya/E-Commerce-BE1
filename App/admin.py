from django.contrib import admin
from .models import Products,Categories,Wishlist,User,Images
# Register your models here.
admin.site.register(Products)
admin.site.register(Categories)
admin.site.register(Wishlist)
admin.site.register(User)
admin.site.register(Images)