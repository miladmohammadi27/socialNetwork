import pickle
import uuid
from bson import ObjectId
from .connector import ProfileDBClientGenerator

"""
class for CRUD operations on profile in mongo
"""
class ProfileDBMS:
    """
    called when user object created in relational db and create
    profile for user in mongo db
    """
    @staticmethod
    def create_profile(userObject):
        with ProfileDBClientGenerator() as client:
            profile_prototype: dict = {
                'user': pickle.dumps(userObject),
                'posts': [
                ]
            }
            result = client.insert_one(profile_prototype)
            userObject.profile_id = result.inserted_id
            userObject.save()

    """
    retrieve users profiles and contains user profile 
    information, posts, comments, likes
    """
    @staticmethod
    def read_profile(userObject):
        with ProfileDBClientGenerator() as client:
            objectID = ObjectId(userObject.profile_id)
            result = client.find_one({"_id": objectID})
            return result


"""
class for CRUD operations on posts in mongo
"""
class PostsDBMS:

    """creates a post in user profile in mongoDB"""
    @staticmethod
    def create_post(userObject, post_text):
        with ProfileDBClientGenerator() as client:
            objectID = ObjectId(userObject.profile_id)

            new_post: dict = {
                "post_uuid": str(uuid.uuid4()),
                "text": post_text,
                "comments": [],
                "likes": []
            }

            result = client.update_one(
                {"_id": objectID},
                {"$push": {"posts": {
                    "$each": [new_post],
                    "$position": 0
                }}}
            )
            return result.upserted_id

    """creates a comment for post in user profile in mongoDB"""
    @staticmethod
    def create_comment(commenterUser, commentText, commenteeUser, commenteePostID):
        with ProfileDBClientGenerator() as client:
            objectID = ObjectId(commenteeUser.profile_id)

            new_comment: dict = {
                "comment_uuid": str(uuid.uuid4()),
                "text": commentText,
                "username": commenterUser.username
            }

            result = client.update_one(
                {"_id": objectID, "posts.post_uuid": commenteePostID},
                {"$push": {"posts.$.comments": {
                    "$each": [new_comment],
                    "$position": 0
                }}}
            )
            return result.upserted_id

    """creates a like for post in user profile in mongoDB"""
    @staticmethod
    def like_post(likerUser, likeeUser, likeePostID):
        with ProfileDBClientGenerator() as client:
            objectID = ObjectId(likeeUser.profile_id)

            result = client.update_one(
                {"_id": objectID, "posts.post_uuid": likeePostID},
                {"$push": {"posts.$.likes": {
                    "$each": [likerUser.username],
                    "$position": 0
                }}}
            )
            return result.upserted_id






