from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from App import views

urlpatterns = [
    # Base route for API overview
    path('', views.getRoutes, name="getRoutes"),
    
    # Product routes
    path('products/', views.getProducts, name="getProducts"),  # List all products
    path('product/<str:pk>', views.getProduct, name="getProduct"),  # Get details of a specific product
    path('products/search/', views.searchProducts, name="searchProducts"),  # Search products

    # User registration and authentication routes
    path('users/register/', views.registerUser, name="register"),  # User registration
    path('users/login/', views.LoginView.as_view(), name='loginApi'),  # User login
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh

    # Protected user routes (require authentication)
    path('users/profile/', views.getUserProfiles, name="getUserProfiles"),  # Get user profile
    path('users/', views.getUsers, name="getUsers"),  # Get all users

    # Account activation route
    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name='activate'),  # Account activation

    # Password reset routes
    path('users/reset-password/', views.requestPasswordReset, name='requestPasswordReset'),  # Request password reset
    path('users/reset-password-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView, name='password_reset_confirm'), # Confirm password reset
    
    # Quantity route
    path('cart/add/',views.add_to_cart, name='addToCart'), 
]
