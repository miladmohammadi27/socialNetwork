from rest_framework import status
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User
from mongoDBMS.dbms import ProfileDBMS, PostsDBMS
from socialApp import serializers


"""
this class is only for testing api, in production and development stage
this class should remove and replace with search users 
"""
class ListAllUsers(ListAPIView):
    permission_classes = [IsAuthenticated]
    model = User
    http_method_names = ['get']
    serializer_class = serializers.UserModelSerializer

    def get_queryset(self):
        return User.objects.all()


"""
goal:
    retrieve profile data of some user that contains user shared posts,
    other users likes and comments on post
inputs:
    user_id is id of user in relational database
output:
    user profile in mongo db that contains all information of user 
    such as posts, comments, likes
"""
class RetrieveUsersProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        wanted_user: User = get_object_or_404(User, pk=request.data['user_id'])
        result: dict = ProfileDBMS.read_profile(wanted_user)
        result.pop('_id')
        result['user'] = wanted_user.username

        return Response({
            'message': 'profile retrieve successfully for wanted user',
            'profile': result
        }, status=status.HTTP_200_OK)


"""
goal:
    user retrieve his own profile data contains all posts and comments and like 
    for the posts
inputs:
    user id in relational db that gets from request
output:
    user profile in mongo db that contains all information of user 
    such as posts, comments, likes
"""
class RetrieveMyProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        result: dict = ProfileDBMS.read_profile(request.user)
        result.pop('_id')
        result['user'] = request.user.username

        return Response({
            'message': 'your profile retrieve successfully',
            'profile': result
        }, status=status.HTTP_200_OK)


"""
goal:
    users can share a post in the social network and 
    other users can see post and comment or like the post
inputs:
    1- user id in relational db that gets from request
    2- text for a post to share with others
output:
    creates a post in user profile document in mongo DB
"""
class CreatePost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user: User = request.user
        post_text: str = request.data['text']
        PostsDBMS.create_post(user, post_text)

        return Response({
            "message": "post created successfully",

        }, status=status.HTTP_201_CREATED)


"""
goal:
    users can let comment on posts that other user was shared
inputs:
    1- commenter_user: user id in relational db for user that wants to let comment
    2- comment_text: text of comment
    3- commentee_id: user id in relational db for user that we want to let comment on his post
    4- commentee_post_id: the id of post that we want to let the comment for it
output:
    creates a comment in post["comments] filed in mongo DB
"""
class CreateComment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        commenter_user: User = request.user
        comment_text: str = request.data['text']
        commentee_id: int = request.data['commentee_id']
        commentee_post_id: int = request.data['commentee_post_id']
        commentee_user = get_object_or_404(User, pk=commentee_id)

        result = PostsDBMS.create_comment(
            commenter_user,
            comment_text,
            commentee_user,
            commentee_post_id
        )

        return Response({
            "message": "comment created successfully",

        }, status=status.HTTP_201_CREATED)


"""
goal:
    users can like a post that other user was shared
inputs:
    1- liker_user: user id in relational db for user that wants to like some post
    3- likee_post_id: a post id for post that we want to like it
    4- likee_id: id of user in relational db that we want to like his post
output:
    creates a like in post["likes] filed in mongo DB
"""
class LikePost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        liker_user: User = request.user
        likee_post_id: int = request.data['likee_post_id']
        likee_id: int = request.data['likee_id']
        likee_user = get_object_or_404(User, pk=likee_id)

        result = PostsDBMS.like_post(
            liker_user,
            likee_user,
            likee_post_id
        )

        return Response({
            "message": "you liked post successfully",

        }, status=status.HTTP_201_CREATED)










