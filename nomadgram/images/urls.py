from django.urls import path
from . import views

app_name = "images"
urlpatterns = [

    #path("all_images/", view = views.ListAllImages.as_view(), name = "all_images"),
    #path("all_comments/", view = views.ListAllComments.as_view(), name = "all_comments"),
    #path("all_likes/", view = views.ListAllLikes.as_view(), name = "all_likes"),
    path("feed/", view = views.Feed.as_view(), name ="feed"),
]
