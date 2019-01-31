from django.conf.urls import url
from . import views

app_name = "images"
'''
urlpatterns = [

    #path("all_images/", view = views.ListAllImages.as_view(), name = "all_images"),
    #path("all_comments/", view = views.ListAllComments.as_view(), name = "all_comments"),
    #path("all_likes/", view = views.ListAllLikes.as_view(), name = "all_likes"),
    path("feed/", view = views.Feed.as_view(), name ="feed"),
]
'''

urlpatterns = [
    url(
        regex=r'^$',
        view = views.Feed.as_view(),
        name = 'feed'
    ),
    url(
        #patterns, regular expressions, regex
        regex = r'(?P<image_id>[0-9]+)/like/',
        view = views.LikeOnImage.as_view(),
        name = 'like_image'
    ),
    url(
        regex = r'(?P<image_id>[0-9]+)/comment/' ,
        view = views.CommentOnImage.as_view(),
        name = 'comment_image'

    )

]