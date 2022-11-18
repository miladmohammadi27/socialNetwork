from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'socialAPP'

urlpatterns = [
    path('users/list/', ListAllUsers.as_view(), name='list_users'),
    path('users/profile/', RetrieveUsersProfile.as_view(), name='retrieve_users_profile'),
    path('my/profile/', RetrieveMyProfile.as_view(), name='retrieve_my_profile'),
    path('create/post/', CreatePost.as_view(), name='create_post'),
    path('create/comment/', CreateComment.as_view(), name='create_comment'),
    path('like/post/', LikePost.as_view(), name='like_post'),
]



