from django.conf.urls import url
from . import views

app_name = "images"

urlpatterns = [
    url(
        regex=r'^$',
        view = views.Feed.as_view(),
        name = 'feed'
    ),
    url(
        #patterns, regular expressions, regex
        regex = r'^(?P<image_id>[0-9]+)/like/$',
        view = views.LikeOnImage.as_view(),
        name = 'like_image'
    ),
    url(
        #patterns, regular expressions, regex
        regex = r'^(?P<image_id>[0-9]+)/unlike/$',
        view = views.UnLikeOnImage.as_view(),
        name = 'like_image'
    ),
    
    url(
        regex = r'^(?P<image_id>[0-9]+)/comments/$' ,
        view = views.CommentOnImage.as_view(),
        name = 'comment_image'
    ),
    url(
        regex = r'^comments/(?P<comment_id>[0-9]+)/$',
        view = views.DeleteComment.as_view(),
        name = 'delete_comment'
    ),
    url(
        regex = r'^(?P<image_id>[0-9]+)/comments/(?P<comment_id>[0-9]+)/$',
        view = views.DeleteCommentOnMine.as_view(),
        name = 'delete_comment_on_mine'
    ),
    url(
        regex = r'^search/$',
        view = views.Search.as_view(),
        name = "search_images"
    )
]