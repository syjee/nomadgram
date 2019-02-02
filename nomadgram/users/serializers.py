from rest_framework import serializers
from . import models
from nomadgram.images import serializers as image_serializers

class ProfileUserSerializer(serializers.ModelSerializer):

    images = image_serializers.ProfileImageSerializer(many=True)

    class Meta:
        model = models.User
        fields = (
            'username',
            'post_count',
            'followers_count',
            'followings_count',
            'name',
            'bio',
            'website',
            'images'
        )


class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'id',
            'profile_image',
            'username',
            'name'
        )