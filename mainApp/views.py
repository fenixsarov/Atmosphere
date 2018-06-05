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
        'darkhalls/darkhall_img_0.jpg',
        'darkhalls/darkhall_img_1.jpg',
        'darkhalls/darkhall_img_2.jpg',
        'darkhalls/darkhall_img_3.jpg',
        'darkhalls/darkhall_img_4.jpg',
        'darkhalls/darkhall_img_5.jpg',
        'darkhalls/darkhall_img_6.jpg',
    ]

    lighthall_imgs = [
        'whitehall/lighthall_img_0.jpg',
        'whitehall/lighthall_img_1.jpg',
        'whitehall/lighthall_img_2.jpg',
        'whitehall/lighthall_img_3.jpg',
        'whitehall/lighthall_img_4.jpg',
        'whitehall/lighthall_img_5.jpg',
        'whitehall/lighthall_img_6.jpg',
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
    plate_text = 'Да, а на фото часть нашей дружной команды. Именно мы радуем Вас дружеской обстановкой и хорошим настроением! Это мы Вас встречаем радушно чаем и печеньками. Мы любим Вас и всегда ждём в нашей тёплой, уютной студии!'
    plate_desc = [{'image': 'gallery/master/1FaQK5pnte8.jpg', 'header': 'ФРУКТОВЫЙ БУКЕТ', 'plate_text': plate_text},
                  {'image': 'gallery/master/7kHQp6mrVfk.jpg', 'header': 'ЛЕТТЕРИНГ', 'plate_text': plate_text},
                  {'image': 'gallery/master/FUZzw8lt8So.jpg', 'header': 'МАСЛЯНАЯ ЖИВОПИСЬ', 'plate_text': plate_text},
                  {'image': 'gallery/master/SmFTgH6yXho.jpg', 'header': 'АКВАРЕЛЬ', 'plate_text': plate_text},
                  {'image': 'gallery/master/YAFDz1ZWNSQ.jpg', 'header': 'КРУЖКА', 'plate_text': plate_text},
                  {'image': 'gallery/master/kbpDgPi_W6A.jpg', 'header': 'SWEETBOX', 'plate_text': plate_text},
                  {'image': 'gallery/master/34lYmz5ASEk.jpg', 'header': 'ФЛОРАРИУМ', 'plate_text': plate_text},
                  {'image': 'gallery/master/8arKte_-Khc.jpg', 'header': 'КИТАЙСКАЯ ЖИВОПИСЬ', 'plate_text': plate_text}
                  ]
    template_name = 'school.pug'
    page_name = 'school'

    def get(self, request):
        return render(request, self.template_name, {'page': self.page_name,
                                                    'plate_desc': self.plate_desc
                                                    })


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
