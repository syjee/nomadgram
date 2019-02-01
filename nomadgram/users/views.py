from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers

class ExploreUsers(APIView):
    def get(self, request, format = None):
        
        last_five = models.User.objects.all().order_by('date_joined')[:5]
        last_five = sorted(last_five, key = lambda x : x.date_joined, reverse=True)
        serializer = serializers.ExploreUserSerializer(last_five, many = True)
        
        return Response(data = serializer.data, status = status.HTTP_200_OK)


class FollowUser(APIView):
    def post(self, request, user_id, format = None):
        
        user = request.user

        try : 
            user_to_follow = models.User.objects.get(id = user_id)
        except models.User.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
        user.followings.add(user_to_follow)
        user.save()

        return Response(status = status.HTTP_200_OK)
            

class UnFollowUser(APIView):
    def post(self, request, user_id, format = None):
        
        user = request.user

        try : 
            user_to_follow = models.User.objects.get(id = user_id)
        except models.User.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
        user.followings.remove(user_to_follow)
        user.save()
        
        return Response(status = status.HTTP_200_OK)
        
        