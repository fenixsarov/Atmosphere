from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.generic import View
from django.template import loader
from precise_bbcode.bbcode import get_parser
from pypugjs.ext.django import loader as pug_loader
from django.conf import settings
from .models import *
import random

# debug = settings.DEBUG


class BaseView(View):
    template_name = 'index.pug'
    page_name = 'index'
    path_prefix = '/static/images/upload_imgs/'

    try:
        bb_parser = get_parser()
    except BaseException:
        print("!")

    def get(self, request):
        return render(request, self.template_name, {'page': self.page_name})


class Main(BaseView):
    template_name = 'index.pug'
    page_name = 'index'


class Team(BaseView):
    template_name = 'team.pug'
    page_name = 'team'


class Blog(BaseView):
    template_name = 'blog.pug'
    page_name = 'blog'


class BlogChange(View):
    plate_desc = []
    pug = ''
    path_prefix = '/static/images/upload_imgs/'

    def get(self, request):
        self.request.session['view'] = self.request.GET['view']
        if self.request.is_ajax():
            self.plate_desc.clear()
            try:
                for ba in BlogArticle.objects.all():
                    self.plate_desc.append({
                        'title': ba.title,
                        'desc': ba.desc,
                        'desc_image': self.path_prefix + ba.desc_image.url,
                        'content': ba.content,
                        'public_date': ba.public_date,
                        'id': ba.pk
                    })
            except BaseException as e:
                print(e)

            pug = loader.render_to_string('mixins/plate_blog.pug',
                                          {'plate_desc': self.plate_desc})

        return JsonResponse({'response': 'ok', 'html': pug})


class BlogSingleArticle(BaseView):
    template_name = 'blog_content.pug'
    page_name = 'blog_article'

    title = ''
    desc = ''
    desc_image = ''
    content = ''
    public_date = ''


    def get(self, request, pk):
        try:
            ba = BlogArticle.objects.get(pk=pk)
            self.title = ba.title
            self.desc = ba.desc
            self.desc_image = self.path_prefix + ba.desc_image
            self.content = ba.content
            self.public_date = ba.public_date

        except BaseException as e:
            print(e)

        return render(
            request, self.template_name, {
                'title': self.title,
                'desc': self.desc,
                'desc_image': self.desc_image,
                'content': self.content,
            }
        )

class PhotoSchool(BaseView):
    template_name = 'school/photo.pug'
    page_name = 'photoschool'


class Halls(BaseView):
    template_name = 'halls.pug'
    page_name = 'halls'
    halls_list = ['dark', 'light']
    darkhall_imgs = []
    lighthall_imgs = []

    def get(self, request):
        try:
            self.darkhall_imgs = [
                self.path_prefix + h.file.url for h in PicHalls.objects.filter(
                    galleryHalls__service_name='dark')
            ]
            self.lighthall_imgs = [
                self.path_prefix + h.file.url for h in PicHalls.objects.filter(
                    galleryHalls__service_name='light')
            ]

        except BaseException as e:
            print(e)

        for i in range(0, random.randint(1, 5)):
            random.shuffle(self.darkhall_imgs)
            random.shuffle(self.lighthall_imgs)

        return render(
            request, self.template_name, {
                'page': self.page_name,
                'halls_list': self.halls_list,
                'darkhall_imgs': self.darkhall_imgs,
                'lighthall_imgs': self.lighthall_imgs
            })


class HallsChange(View):
    darkhall_imgs = []
    lighthall_imgs = []
    list_imgs = []
    halls_list = ['dark', 'light']
    path_prefix = '/static/images/upload_imgs/'
    title = ''
    desc = ''
    hallsize = ''
    price = -1
    pug = ''
    bb_parser = get_parser()

    def get(self, request):
        self.request.session['view'] = self.request.GET['view']

        if self.request.is_ajax:
            for i in self.halls_list:
                if self.request.session['view'] == i:
                    self.list_imgs = [
                        self.path_prefix + h.file.url for h in PicHalls.objects.filter(
                            galleryHalls__service_name=i)
                    ]

                    random.shuffle(self.list_imgs)

                    hall = Hall.objects.get(service_name=i)
                    self.title = hall.title.upper()
                    self.desc = self.bb_parser.render(hall.desc)
                    self.price = hall.price
                    self.hallsize = hall.hall_size

                pug = loader.render_to_string(
                    'includes/universal_slider_inc.html',
                    {'imgs_list': self.list_imgs})

            return JsonResponse({
                'response': 'ok',
                'html': pug,
                'title': self.title,
                'desc': self.desc,
                'hallsize': self.hallsize,
                'price': self.price
            })

        return HttpResponse('ok', content_type='text/html')


class Graduations(BaseView):
    template_name = 'graduations.pug'
    page_name = 'graduations'
    main_text = ''
    title = ''
    desc_image = ''

    def get(self, request):

        if self.request.is_ajax():
            try:
                # Getting data for page description (title, description, image)
                obj = DescriptionsList.objects.get(service_name=self.page_name)
                self.title = obj.title
                # self.main_text = obj.desc

                self.main_text = self.bb_parser.render(obj.desc)
                self.desc_image = self.path_prefix + obj.file.url
                self.title = self.title.upper()

            except BaseException as e:
                print(e)
            return JsonResponse({
                'response': 'ok',
                'image_src': self.desc_image,
                'title': self.title,
                'main_text': self.main_text
            })

        return render(request, self.template_name, {'page': self.page_name})


class GraduationsChange(View):
    path_prefix = '/static/images/upload_imgs/'

    def get(self, request):
        self.request.session['view'] = self.request.GET['view']
        gallery_imgs = []
        html = ''
        if self.request.is_ajax:
            if self.request.session['view'] == 'school':
                for img in PicGraduations.objects.filter(
                        galleryGraduations__service_name='school'):
                    gallery_imgs.append(self.path_prefix + img.file.url)

            elif self.request.session['view'] == 'kindergarten':
                for img in PicGraduations.objects.filter(
                        galleryGraduations__service_name='kindergarten'):
                    gallery_imgs.append(self.path_prefix + img.file.url)

            elif self.request.session['view'] == 'printing':
                for img in PicGraduations.objects.filter(
                        galleryGraduations__service_name='printing'):
                    gallery_imgs.append(self.path_prefix + img.file.url)

            pug = loader.render_to_string('mixins/photogallery_item.pug',
                                          {'gallery_imgs': gallery_imgs})
            # html = loader.render_to_string('mixins/photogallery_item_inc.html', {'gallery_imgs': gallery_imgs}, request=request)

        return JsonResponse({'response': 'ok', 'html': pug})


class Sessions(BaseView):
    template_name = 'sessions.pug'
    page_name = 'sessions'

    def get(self, request):
        return render(request, self.template_name, {
            'page': self.page_name,
        })


class SessionsChange(BaseView):
    list_imgs = []
    session_list = ['family', 'individual', 'child', 'portrait', 'lovestory']
    title = ''
    desc = ''
    pug = ''
    path_prefix = '/static/images/upload_imgs/'

    def get(self, request):
        self.request.session['view'] = self.request.GET['view']

        if self.request.is_ajax:
            for i in self.session_list:
                if self.request.session['view'] == i:
                    self.list_imgs = [
                        self.path_prefix + h.file.url for h in PicSession.objects.filter(
                            gallerySession__service_name=i)
                    ]

                    random.shuffle(self.list_imgs)

                    session = Session.objects.get(service_name=i)
                    self.title = session.title.upper()
                    self.desc = self.bb_parser.render(session.desc)

            pug = loader.render_to_string('includes/universal_slider_inc.html',
                                          {'imgs_list': self.list_imgs})

            return JsonResponse({
                'response': 'ok',
                'html': pug,
                'title': self.title,
                'desc': self.desc,
            })

        return HttpResponse('ok', content_type='text/html')


class School(BaseView):
    template_name = 'school.pug'
    page_name = 'school'
    # main_text = 'Да, а на фото часть нашей дружной команды. Именно мы радуем Вас дружеской обстановкой и хорошим настроением! Это мы Вас встречаем радушно чаем и печеньками. Мы любим Вас и всегда ждём в нашей тёплой, уютной студии!'

    main_text = ''
    title = ''
    desc_image = []
    school_imgs = []

    def get(self, request):
        if self.request.is_ajax():
            try:
                # Getting data for page description (title, description, image)
                obj = DescriptionsList.objects.get(service_name=self.page_name)
                self.title = obj.title
                self.main_text = self.bb_parser.render(obj.desc)
                self.desc_image = self.path_prefix + obj.file.url
                self.title = self.title.upper()

            except BaseException as e:
                print(e)
            return JsonResponse({
                'response': 'ok',
                'image_src': self.desc_image,
                'title': self.title,
                'main_text': self.main_text
            })

        return render(
            request,
            self.template_name,
            {
                'page': self.page_name,
                'school_imgs': self.school_imgs,
                # 'main_text': self.main_text,
                # 'title': self.title,
                # 'desc_image': self.desc_image
            })


class MasterClass(BaseView):
    template_name = 'masterclass.pug'
    page_name = 'masterclass'
    plate_desc = []
    main_text = ''
    title = ''
    desc_image = ''

    def get(self, request):
        if self.request.is_ajax():
            try:
                # Getting data for page description (title, description, image)
                obj = DescriptionsList.objects.get(service_name=self.page_name)
                self.title = obj.title

                self.main_text = self.bb_parser.render(obj.desc)
                self.desc_image = self.path_prefix + obj.file.url
                self.title = self.title.upper()

            except BaseException as e:
                print(e)
            return JsonResponse({
                'response': 'ok',
                'image_src': self.desc_image,
                'title': self.title,
                'main_text': self.main_text
            })

        return render(request, self.template_name, {
            'page': self.page_name,
            'plate_desc': self.plate_desc,
        })


class SingleMasterClass(BaseView):
    template_name = 'single_masterclass.pug'
    page_name = 'single_masterclass'
    plate_desc = []
    main_text = ''
    title = ''
    desc_image = ''
    full_desc = ''
    mc = ''
    pug = ''
    list_imgs = []
    bb_parser = get_parser()

    def get(self, request, pk):
        arg = self.args
        try:
            self.list_imgs.clear()
            mc = Masterclass.objects.get(pk=pk)
            self.title = mc.title
            self.full_desc = self.bb_parser.render(mc.full_desc)

            # self.list_imgs = [h.file.url for h in PicMasterclass.objects.filter(galleryMasterclass_id=pk)]

            self.list_imgs.append(self.path_prefix + mc.desc_image.url)
            random.shuffle(self.list_imgs)

            self.pug = loader.render_to_string(
                'includes/universal_slider_inc.html',
                {'imgs_list': self.list_imgs})

        except BaseException as e:
            print(e)

        return render(
            request, self.template_name, {
                'page': self.page_name,
                'header': self.title,
                'desc': self.full_desc,
                'pug': self.pug
            })


class MasterClassChange(View):
    plate_desc = []
    path_prefix = '/static/images/upload_imgs/'

    def get(self, request):
        self.request.session['view'] = self.request.GET['view']
        if self.request.is_ajax:
            self.plate_desc.clear()
            try:
                for mc in Masterclass.objects.all():
                    self.plate_desc.append({
                        'image': self.path_prefix + mc.desc_image.url,
                        'title': mc.title,
                        'desc': mc.short_desc,
                        'id': mc.pk
                    })
            except BaseException as e:
                print(e)

            pug = loader.render_to_string('mixins/plate_masterclass.pug',
                                          {'plate_desc': self.plate_desc})

        return JsonResponse({'response': 'ok', 'html': pug})


# Может ещё нужно что-то поменять... но так работает)
class ReservedForm(View):
    def get(self, request):
        if self.request.is_ajax:
            pug = loader.render_to_string('includes/reserved_inc.pug', {})

        return JsonResponse({'response': 'ok', 'html': pug})


class Events(BaseView):
    template_name = 'events.pug'
    page_name = 'events'


class About(BaseView):
    template_name = 'about.pug'
    page_name = 'about'


class AboutChange(View):
    plate_desc = []
    pug = ''
    path_prefix = '/static/images/upload_imgs/'

    def get(self, request):
        # self.request.session['view'] = self.request.GET['view']
        if self.request.is_ajax():
            self.plate_desc.clear()
            try:
                for tm in TeamPerson.objects.all():
                    self.plate_desc.append({
                        'title': tm.title,
                        'desc': tm.desc,
                        'desc_image': self.path_prefix + tm.desc_image.url,
                        'content': tm.content,
                    })
            except BaseException as e:
                print(e)

            pug = loader.render_to_string('mixins/plate_teamperson.pug',
                                          {'plate_desc': self.plate_desc})
            return JsonResponse({'response': 'ok', 'html': pug})

# class Useful(BaseView):
#     template_name = 'useful.pug'
#     page_name = 'useful'
#     # plate_text = 'Да, а на фото часть нашей дружной команды. Именно мы радуем Вас дружеской обстановкой и хорошим настроением! Это мы Вас встречаем радушно чаем и печеньками. Мы любим Вас и всегда ждём в нашей тёплой, уютной студии!'
#
#     main_imgs = ['useful/useful_main_img_0.jpg']
#     plate_desc = []
#
#     main_text = ''
#     title = ''
#     desc_image = ''
#
#     try:
#         for article in UsefulArticle.objects.all():
#             plate_desc.append({
#                 'image': BaseView.path_prefix + article.desc_image.url,
#                 'header': article.title,
#                 'plate_text': article.desc
#             })
#     except BaseException as e:
#         print(e)
#
#     def get(self, request):
#         if self.request.is_ajax():
#             try:
#                 # Getting data for page description (title, description, image)
#                 obj = DescriptionsList.objects.get(service_name=self.page_name)
#                 self.title = obj.title
#                 self.main_text = self.bb_parser.render(obj.desc)
#                 self.desc_image = self.path_prefix + obj.file.url
#                 self.title = self.title.upper()
#
#             except BaseException as e:
#                 print(e)
#             return JsonResponse({
#                 'response': 'ok',
#                 'image_src': self.desc_image,
#                 'title': self.title,
#                 'main_text': self.main_text
#             })
#         return render(request, self.template_name, {
#             'page': self.page_name,
#             'plate_desc': self.plate_desc
#         })


class UsefulChange(View):
    plate_desc = []
    pug = ''
    bb_parser = get_parser()
    path_prefix = '/static/images/upload_imgs/'

    def get(self, request):
        self.request.session['view'] = self.request.GET['view']
        if self.request.is_ajax:
            self.plate_desc.clear()

            try:
                for article in UsefulArticle.objects.all():
                    self.plate_desc.append({
                        'image': self.path_prefix + article.desc_image.url,
                        'header': article.title,
                        'plate_text': self.bb_parser.render(article.desc)
                    })

            except BaseException as e:
                print(e)

            self.pug = loader.render_to_string('mixins/plate_useful.pug',
                                               {'plate_desc': self.plate_desc})

        return JsonResponse({'response': 'ok', 'html': self.pug})

# Create your views here.
