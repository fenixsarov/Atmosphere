from django.shortcuts import render
from django.http import HttpResponse
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
    halls_list = ['dark', 'light']
    darkhall_imgs = [
        '/images/darkhalls/darkhall_img_0.jpg',
        '/images/darkhalls/darkhall_img_1.jpg',
        '/images/darkhalls/darkhall_img_2.jpg',
        '/images/darkhalls/darkhall_img_3.jpg',
        '/images/darkhalls/darkhall_img_4.jpg',
        '/images/darkhalls/darkhall_img_5.jpg',
        '/images/darkhalls/darkhall_img_6.jpg',
    ]

    lighthall_imgs = [
        '/images/whitehall/lighthall_img_0.jpg',
        '/images/whitehall/lighthall_img_1.jpg',
        '/images/whitehall/lighthall_img_2.jpg',
        '/images/whitehall/lighthall_img_3.jpg',
        '/images/whitehall/lighthall_img_4.jpg',
        '/images/whitehall/lighthall_img_5.jpg',
        '/images/whitehall/lighthall_img_6.jpg',
    ]

    def get(self, request):
        return render(request, self.template_name, {'page': self.page_name,
                                                    'halls_list': self.halls_list,
                                                    'darkhall_imgs': self.darkhall_imgs,
                                                    'lighthall_imgs': self.lighthall_imgs})


class HallsChange(View):
    def get(self, request):
        self.request.session['view'] = self.request.GET['view']
        return HttpResponse('ok', content_type='text/html')


class Graduations(BaseView):
    template_name = 'graduations.pug'
    page_name = 'graduations'


class Sessions(BaseView):
    template_name = 'sessions.pug'
    page_name = 'sessions'


class SessionsChange(BaseView):
    # template_name = 'halls.pug'
    # page_name = 'halls'
    def get(self, request):
        self.request.session['view'] = self.request.GET['view']
        return HttpResponse('ok', content_type='text/html')


class School(BaseView):
    template_name = 'school.pug'
    page_name = 'school'


class MasterClass(BaseView):
    template_name = 'masterclass.pug'
    page_name = 'masterclass'


class Events(BaseView):
    template_name = 'events.pug'
    page_name = 'events'


class About(BaseView):
    template_name = 'about.pug'
    page_name = 'about'


class Useful(BaseView):
    template_name = 'useful.pug'
    page_name = 'useful'

# Create your views here.
