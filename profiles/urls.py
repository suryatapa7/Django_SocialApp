from django.urls import path
from .views import ProfileDetailView, FollowView, EditProfileView


app_name = 'profiles'

urlpatterns = [
    path('profile/<str:username>/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('<str:username>/follow/', FollowView.as_view(), name='follow'),
    path('<str:username>/', ProfileDetailView.as_view(), name='detail'),
]

