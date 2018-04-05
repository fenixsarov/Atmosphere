from django.shortcuts import render
from django.views.generic import View
from django.conf import settings

# debug = settings.DEBUG

class BaseView(View):
    template_name = 'index.pug'
    page_name = 'index'

    def get(self, request):
        return render(request, self.template_name, {'page': self.page_name})


class Main(BaseView):
    template_name = 'index.pug'
    page_name = 'index'


class Halls(BaseView):
    template_name = 'halls.pug'
    page_name = 'halls'


class Graduations(BaseView):
    template_name = 'graduations.pug'
    page_name = 'graduations'


class Sessions(BaseView):
    template_name = 'sessions.pug'
    page_name = 'sessions'


class School(BaseView):
    template_name = 'school.pug'
    page_name = 'school'


class Events(BaseView):
    template_name = 'events.pug'
    page_name = 'events'


class About(BaseView):
    template_name = 'about.pug'
    page_name = 'about'



# Create your views here.
