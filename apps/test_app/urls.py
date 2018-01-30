from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
  url(r'^$', views.index, name = "index"),
  url(r'^user_login$',views.user_login, name = "user_login"),
  url(r'^create_user$',views.create_user, name = "create_user"),
  url(r'^travels$',views.travels, name = "travels"),
  url(r'^add_trip_get$',views.add_trip_get, name = "add_trip_get"),
  url(r'^add_trip_post$',views.add_trip_post, name = "add_trip_post"),
  url(r'^join_trip/(?P<trip_id>\d+)$',views.join_trip, name = "join_trip"),
  url(r'^trip_details/(?P<trip_id>\d+)$',views.trip_details, name = "trip_details"),
  url(r'^log_out$',views.log_out, name = "log_out"),

]