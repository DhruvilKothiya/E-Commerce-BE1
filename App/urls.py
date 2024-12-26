from App import views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser

urlpatterns = [
    path('', views.getRoutes, name="getRoutes"),
    path('products/', views.getProducts, name="getProducts"),
    path('product/<str:pk>', views.getProduct, name="getProduct"),
    path('users/register/', views.registerUser, name="register"),
    path('users/login/',views.LoginView.as_view(), name='loginApi'), 
    # Token refresh
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Protected routes
    path('users/profile/', views.getUserProfiles, name="getUserProfiles"),
    path('users/', views.getUsers, name="getUsers"),
    
    # Account activation
    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name='activate'),
    
    # Password reset
    path('users/reset-password/', views.requestPasswordReset, name='requestPasswordReset'),
    path('users/reset-password-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView, name='password_reset_confirm'),

    #Search route
    path('products/search/', views.searchProducts, name="searchProducts"),

]

