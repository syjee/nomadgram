from django.conf.urls import url
from . import views

app_name = "notifications"

urlpatterns = [
    url(
        regex=r'^$',
        view = views.Notify.as_view(),
        name = 'notify'
    ),
]
