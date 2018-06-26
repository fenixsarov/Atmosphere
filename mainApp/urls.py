from django.conf.urls import url
#from mainApp import views
from mainApp.views import *

urlpatterns = (
    # url(r'^$', views.main, name='index'),
    url(r'^$', Main.as_view()),
    url(r'^halls/$', Halls.as_view()),
    url(r'^halls/hallschange/$', HallsChange.as_view(), name='hallschange'),
    url(r'^graduations/$', Graduations.as_view()),
    url(r'^graduations/graduationschange/$', GraduationsChange.as_view(), name='graduationschange'),
    url(r'^sessions/$', Sessions.as_view()),
    url(r'^halls/sessionschange/$', SessionsChange.as_view(), name='sessionschange'),
    url(r'^school/$', School.as_view()),
    url(r'^masterclass/$', MasterClass.as_view()),
    url(r'^events/$', Events.as_view()),
    url(r'^about/$', About.as_view()),
    url(r'^useful/$', Useful.as_view()),
)


