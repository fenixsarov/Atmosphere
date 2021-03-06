from django.conf.urls import url
# from mainApp import views
from mainApp.views import *
from django.views.generic import TemplateView

urlpatterns = (
    # url(r'^$', views.main, name='index'),
    url(r'^$', Main.as_view()),
    url(r'^halls/$', Halls.as_view()),
    url(r'^halls/hallschange/$', HallsChange.as_view(), name='hallschange'),
    url(r'^graduations/$', Graduations.as_view()),
    url(r'^graduations/graduationschange/$', GraduationsChange.as_view(),
        name='graduationschange'),
    url(r'^sessions/$', Sessions.as_view()),
    url(r'^halls/sessionschange/$', SessionsChange.as_view(),
        name='sessionschange'),
    url(r'^school/$', School.as_view()),
    url(r'^school/photo/$', PhotoSchool.as_view()),
    url(r'^school/study_photography/$', StudyPhotography.as_view()),
    url(r'^masterclass/$', MasterClass.as_view()),
    url(r'^masterclass/(?P<pk>\d+)/$', SingleMasterClass.as_view(),
        name='single_mc'),
    url(r'^masterclass/masterclasschange/$', MasterClassChange.as_view(),
        name='masterclasschange'),
    url(r'^reserved/form/$', ReservedForm.as_view(), name='reserved'),
    url(r'^events/$', Events.as_view()),
    url(r'^about/$', About.as_view()),
    url(r'^about/aboutchange/$', AboutChange.as_view(), name='aboutchange'),
    url(r'^team/$', Team.as_view()),
    url(r'^blog/$', Blog.as_view()),
    url(r'^blog/blogchange/$', BlogChange.as_view(), name='blogchange'),
    url(r'^blog/(?P<pk>\d+)/$', BlogSingleArticle.as_view(), name='blog_article'),
    url(r'^reserve/$', ReservedForm.as_view()),
    url(r'^robots\.txt$', TemplateView.as_view( template_name='robots.txt', content_type='text/plain' ))
)
