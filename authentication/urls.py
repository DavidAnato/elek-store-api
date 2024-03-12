from django.urls import path
from .views import LoginView, LogoutView, SignupView, PasswordResetView, UserProfileUpdateView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('profile/', UserProfileUpdateView.as_view(), name='profile'),

]
