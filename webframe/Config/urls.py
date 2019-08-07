from Tesla.urls import path

from Main import views
urlpatterns = [
    path('/index/',views.index),
]