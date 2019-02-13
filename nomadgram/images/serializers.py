from rest_framework import serializers
from . import models
from nomadgram.users import models as user_models

class FeedUserSerializeer(serializers.ModelSerializer):
    
    class Meta:
        model = user_models.User
        fields = (
            'username',
            'profile_image'
        )

class CommentSerializer(serializers.ModelSerializer):

    creator = FeedUserSerializeer(read_only = True)

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'creator',
            'message'
        )



class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Like
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):

    #comments_set
    comments = CommentSerializer(many=True)
    creator = FeedUserSerializeer()

    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'location',
            'caption',
            'comments',
            'like_count',
            'creator'
        )


class ProfileImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'like_count',
            'comment_count'
        )

class SmallImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = ('file',)