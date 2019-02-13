from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from nomadgram.notifications import views as notify_views


class Feed(APIView):
    def get(self, request, format = None):
        user = request.user
        following_users = user.followings.all()

        image_list = []

        for following_user in following_users:
            
            user_images = following_user.images.all()[:2]
            for image in user_images:
                image_list.append(image)

        sorted_list = sorted(image_list, key = lambda x : x.created_at, reverse=True)
        
        serializer = serializers.ImageSerializer(sorted_list, many = True)

        return Response(serializer.data)

class UnLikeOnImage(APIView):
    def delete(self, reqeust, image_id, format = None):
        user = reqeust.user
        
        try:
            found_image = models.Image.objects.get(id = image_id)
        except models.Image.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        try : 
            found_like = models.Like.objects.get(
                creator = user,
                image = found_image
                )
            found_like.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)

        except models.Like.DoesNotExist : 
            return Response(status = status.HTTP_304_NOT_MODIFIED)


class LikeOnImage(APIView):
    def post(self, request, image_id, format = None):

        user = request.user

        try:
            found_image = models.Image.objects.get(id=image_id)
            
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preexisting_like = models.Like.objects.get(
                creator=user,
                image=found_image
            )
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        except models.Like.DoesNotExist:
            new_like = models.Like.objects.create(
                creator=user,
                image=found_image
            )
            new_like.save()
            notify_views.create_notification(user,"like", found_image.creator, found_image)
            return Response(status=status.HTTP_201_CREATED)


class CommentOnImage(APIView):
    def post(self,request,image_id,format = None):
        
        user = request.user
        
        try:
            found_image = models.Image.objects.get(id = image_id)
        except models.Image.DoesNotExist:
            return Response(status = status.HTTP_404)

        serializer = serializers.CommentSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save(creator = user, image = found_image)
            notify_views.create_notification(user, "comment", found_image.creator, found_image, serializer.data['message'])
            return Response(data = serializer.data, status = status.HTTP_201_CREATED)

        else :
            return Response(data=serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class DeleteComment(APIView):
    def delete(self, request, comment_id, format = None):
        user = request.user

        try:
            found_comment = models.Comment.objects.get(id = comment_id,creator = user)
            found_comment.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)

        except models.Comment.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

    
class Search(APIView):
    def get (self, request, format = None):

        hashtags = request.query_params.get('hashtags','None')
        if hashtags != None : 
            hashtags = hashtags.split(",")

            images = models.Image.objects.filter(tags__name__in=hashtags).distinct()
            
            serializer = serializers.ProfileImageSerializer(images, many = True)

            return Response(data = serializer.data, status = status.HTTP_200_OK)

        else: return Response(status = status.HTTP_400_BAD_REQUEST)