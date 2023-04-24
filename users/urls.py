from django.contrib.auth import views as auth_views
from django.urls import path,include

from . import views

app_name = 'users'

urlpatterns = [

    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('profile/', views.profile, name="profile"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('update_profile/', views.update_profile, name="update_profile"),
    path('logout/', views.logout, name="logout"),
    path('follow_users/', views.follow_users, name="follow_users"),
    path('follow/(<followee_id>)/', views.follow, name="follow"),
    path('unfollow/(<followee_id>)/', views.unfollow, name="unfollow"),
    path('my_followers/', views.my_followers, name="my_followers"),
    path('follower_profile/(<follower_id>)/', views.follower_profile, name="follower_profile")
]
