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

        my_images = user.images.all()[:2]
        for image in my_images :
            image_list.append(image)

        sorted_list = sorted(image_list, key = lambda x : x.created_at, reverse=True)
        
        serializer = serializers.ImageSerializer(sorted_list, many = True)

        return Response(status = status.HTTP_200_OK,data = serializer.data)

class getImage(APIView):

    def find_own_image(self, image_id, user):
        try: 
            my_image = models.Image.objects.get(id = image_id, creator = user)
            return my_image
        except models.Image.DoesNotExist :
            return None


    def get(self, request, image_id, format = None):
        
        try:
            found_image = models.Image.objects.get(id = image_id)
            serializer = serializers.ImageSerializer(found_image)
            return Response(status = status.HTTP_200_OK, data= serializer.data)

        except models.Image.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)


    # modify
    def put(self, request, image_id, format  = None):
        user = request.user

        image_to_update =  self.find_own_image(image_id, user)
        if image_to_update is None:
            return Response(status = status.HTTP_401_UNAUTHORIZED)
        
        serializer = serializers.InputImageSerializer(image_to_update, data = request.data, partial = True)

        if serializer.is_valid():
            serializer.save(creator = user)
            return Response(status = status.HTTP_200_OK)

        else : return Response(status = status.HTTP_400_BAD_REQUEST)

            

    def delete(self, request, image_id, format = None):
        user = request.user

        image_to_delete = self.find_own_image(image_id, user)
        if image_to_delete is None:
            return Response(status = status.HTTP_401_UNAUTHORIZED)

        image_to_delete.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


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

class LikeDetailsOnImage(APIView):
    def get(self, request, image_id, format = None):

        try : 
            found_image = models.Image.objects.get(id = image_id)
            found_likes = found_image.likes.all()

            user_list = []

            for like in found_likes :
                user_list.append(like.creator)
            
            serializer = serializers.FeedUserSerializeer(user_list, many = True)
            
            return Response(status = status.HTTP_200_OK, data = serializer.data)

        except models.Image.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)


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

        except models.Comment.DoesNotExist:
            return Response(status = status.HTTP_400_BAD_REQUEST)
           
        return Response(status = status.HTTP_204_NO_CONTENT)

class DeleteCommentOnMine(APIView):
    def delete(self, request, image_id, comment_id, format = None):
        user = request.user

        try:
            comment_to_delete  = models.Comment.objects.get(id = comment_id, image__id = image_id, image__creator = user)
            comment_to_delete.delete()
            
        except models.Comment.DoesNotExist :
            return Response(status = status.HTTP_400_BAD_REQUEST)

        return Response(status = status.HTTP_204_NO_CONTENT)

class Search(APIView):
    def get (self, request, format = None):

        hashtags = request.query_params.get('hashtags','None')
        if hashtags != None : 
            hashtags = hashtags.split(",")

            images = models.Image.objects.filter(tags__name__in=hashtags).distinct()
            
            serializer = serializers.ProfileImageSerializer(images, many = True)

            return Response(data = serializer.data, status = status.HTTP_200_OK)

        else: return Response(status = status.HTTP_400_BAD_REQUEST)