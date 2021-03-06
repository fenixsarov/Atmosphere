from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.generic import View
from django.template import loader
from precise_bbcode.bbcode import get_parser
from django.core.mail import send_mail
from pypugjs.ext.django import loader as pug_loader
from django.conf import settings
from .models import *
import random
from django.core.mail import EmailMessage

# debug = settings.DEBUG


class BaseView(View):
    template_name = 'index.pug'
    page_name = 'index'
    path_prefix = '/static/images/upload_imgs/'

    try:
        bb_parser = get_parser()
    except BaseException as e:
        print(e)

    def get_feedback(self):
        # More questions?
        return [f.desc for f in Feedback.objects.all()][0]


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

                self.plate_desc.reverse()

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
    list_imgs = []
    public_date = ''

    def get(self, request, pk):
        try:
            ba = BlogArticle.objects.get(pk=pk)
            self.title = ba.title
            self.desc = ba.desc
            self.desc_image = self.path_prefix + ba.desc_image.url
            # self.content = ba.content
            self.public_date = ba.public_date
            self.content = ba.content

            # Looking for related teachers
            # content = [c for c in ba.content.all()]
            # self.content.clear()
            # for c in content:
            #     src_img = ''
            #     try:
            #         src_img = '/images/upload_imgs/' + c.desc_image.url
            #     except BaseException as e:
            #         print(e)
            #         print('Normal continue work...')

                # self.content.append({
                #     'title': c.title,
                #     'content': c.content,
                #     'desc_image': src_img,
                # })

            # self.teachers = [t for t in mc.teachers.all()]
            self.list_imgs.clear()
            self.list_imgs = [self.path_prefix + h.file.url for h in
                              PicBlogArticle.objects.filter(galleryBlogArticle_id=pk)]

        except BaseException as e:
            print(e)

        return render(
            request, self.template_name, {
                'title': self.title,
                'desc': self.desc,
                'desc_image': self.desc_image,
                'content': self.content,
                'list_imgs': self.list_imgs,
                'public_date': self.public_date

            }
        )


class PhotoSchool(BaseView):
    template_name = 'school/photo.pug'
    page_name = 'photoschool'
    # id = -1
    # title = ''
    # short_desc = ''
    # full_desc = ''
    # desc_image = ''
    # price = -1
    # who_interested = ''
    teachers = []
    # course_program = []
    # constructor = ''
    # start_date = ''
    # list_imgs = []
    # course_blocks = []
    #
    def get(self, request):
    #    try:

    #         self.list_imgs.clear()
    #         ps = PhotoFromScratch.objects.get(pk=1)
    #         self.id = 1
    #         self.title = ps.title
    #         self.full_desc = ps.full_desc
    #         self.desc_image = self.path_prefix + ps.desc_image.url
    #         self.price = ps.price
    #         self.who_interested = ps.who_interested
    #         # Looking for related teachers
    #         teachers = [t for t in ps.teachers.all()]
    #         self.teachers.clear()
    #         for t in teachers:
    #             self.teachers.append({
    #                 'title': t.title,
    #                 'desc': t.desc,
    #                 'content': t.content,
    #                 'desc_image': self.path_prefix + t.desc_image.url,
    #                 'social_link': t.social_link,
    #                 'social_name': t.social_name,
    #             })
    #
    #         # Course program
    #         course_program_course = [c for c in ps.course_program.course.all()]
    #         for c in course_program_course:
    #             self.course_blocks.append({
    #                 'intro': c.intro,
    #                 'title': c.title,
    #                 'desc': c.desc,
    #                 'teacher': c.teacher.all()[0].title,
    #                 'desc_image': c.desc_image
    #             })
    #
    #         self.list_imgs.clear()
    #         self.list_imgs = [self.path_prefix + h.file.url for h in
    #                           PicPhotoFromScratch.objects.filter(galleryMasterclass_id=1)]
    #
    #         random.shuffle(self.list_imgs)
    #
    #    except BaseException as e:
    #       print(e)

        return render(request, self.template_name, {
                'page': self.page_name,
                # 'title': self.title,
                # 'full_desc': self.full_desc,
                # 'desc_image': self.desc_image,
                # 'price': self.price,
                # 'who_interested': self.who_interested,
                # 'teachers': self.teachers,
                # 'course_blocks': self.course_blocks,
                # 'list_imgs': self.list_imgs,
                'feedback': self.get_feedback(),
            }
        )

class StudyPhotography(BaseView):
    template_name = 'school/studio_photo.pug'
    page_name = 'studiophoto'
    id = -1
    title = ''
    short_desc = ''
    full_desc = ''
    desc_image = ''
    price = -1
    who_interested = ''
    teachers = []
    course_intro = ''
    course_program = []
    constructor = ''
    start_date = ''
    list_imgs = []
    course_blocks = []

    def get(self, request):
        try:
            self.list_imgs.clear()
            pc = PhotoCourses.objects.get(pk=1)
            self.id = 1
            self.title = pc.title
            self.full_desc = pc.full_desc
            self.desc_image = self.path_prefix + pc.desc_image.url
            self.price = pc.price
            self.who_interested = pc.who_interested

            # Looking for related teachers
            teachers = [t for t in pc.teachers.all()]
            self.teachers.clear()
            for t in teachers:
                self.teachers.append({
                    'title': t.title,
                    'desc': t.desc,
                    'content': t.content,
                    'desc_image': self.path_prefix + t.desc_image.url,
                    'social_link': t.social_link,
                    'social_name': t.social_name,
                })

            # Course program
            course_program_course = [c for c in pc.course_program.course.all()]
            self.course_intro = pc.course_program.intro
            self.course_blocks.clear()
            for c in course_program_course:
                self.course_blocks.append({
                    'title': c.title,
                    'desc': c.desc,
                    'teacher': c.teacher.all()[0].title,
                    'desc_image': self.path_prefix + c.desc_image.url
                })

            # Course images
            self.list_imgs.clear()
            self.list_imgs = [self.path_prefix + h.file.url for h in
                              PicPhotoCourses.objects.filter(galleryMasterclass_id=1)]

            random.shuffle(self.list_imgs)

        except BaseException as e:
            print(e)

        return render(request, self.template_name, {
            'page': self.page_name,
            'title': self.title,
            'full_desc': self.full_desc,
            'desc_image': self.desc_image,
            'price': self.price,
            'who_interested': self.who_interested,
            'teachers': self.teachers,
            'course_intro': self.course_intro,
            'course_blocks': self.course_blocks,
            'list_imgs': self.list_imgs,
            'feedback': self.get_feedback(),
            }
        )

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
                    self.desc = hall.desc
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

                self.main_text = obj.desc
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
                    self.desc = session.desc

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
    prelude = ''

    def get(self, request):
        obj = DescriptionsList.objects.get(service_name=self.page_name)
        self.prelude = obj.prelude
        if self.request.is_ajax():
            try:
                # Getting data for page description (title, description, image)
                obj = DescriptionsList.objects.get(service_name=self.page_name)
                self.title = obj.title
                # self.main_text = self.bb_parser.render(obj.desc)
                self.main_text = obj.desc
                self.desc_image = self.path_prefix + obj.file.url
                self.title = self.title.upper()
                self.prelude = obj.prelude


            except BaseException as e:
                print(e)
            return JsonResponse({
                'response': 'ok',
                'image_src': self.desc_image,
                'title': self.title,
                'main_text': self.main_text,
                'prelude': self.prelude
            })

        return render(
            request,
            self.template_name,
            {
                'page': self.page_name,
                'school_imgs': self.school_imgs,
                'prelude': self.prelude
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
    prelude = ''

    def get(self, request):
        obj = DescriptionsList.objects.get(service_name=self.page_name)
        self.prelude = obj.prelude

        if self.request.is_ajax():
            try:
                # Getting data for page description (title, description, image)
                obj = DescriptionsList.objects.get(service_name=self.page_name)
                self.title = obj.title

                # self.main_text = self.bb_parser.render(obj.desc)
                self.main_text = obj.desc
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
            'prelude': self.prelude
        })


class SingleMasterClass(BaseView):
    template_name = 'single_masterclass.pug'
    page_name = 'single_masterclass'
    id = -1
    plate_desc = []
    main_text = ''
    teachers = []
    title = ''
    desc_image = ''
    full_desc = ''
    price = 0
    mc = ''
    pug = ''
    list_imgs = []
    video = ''
    who_i = ''
    list_feedbacks = []
    feedback = ''

    def get(self, request, pk):
        arg = self.args
        try:
            self.list_imgs.clear()
            mc = Masterclass.objects.get(pk=pk)
            self.id = pk
            self.title = mc.title
            # self.full_desc = self.bb_parser.render(mc.full_desc)
            self.full_desc = mc.full_desc
            self.price = mc.price
            self.desc_image = self.path_prefix + mc.desc_image.url
            self.video = mc.video
            self.who_i = mc.who_interested

            # Feedback
            feedbacks = [f for f in mc.feedback.all()]
            self.list_feedbacks.clear()
            for f in feedbacks:
                self.list_feedbacks.append({
                    'user_name': f.name,
                    'user_feedback': f.feedback,
                    'user_img': self.path_prefix + f.image.url,
                    'user_vklink': f.vklink
                })

            # Looking for related teachers
            teachers = [t for t in mc.teachers.all()]
            self.teachers.clear()
            for t in teachers:
                self.teachers.append({
                    'title': t.title,
                    'desc': t.desc,
                    'content': t.content,
                    'desc_image': self.path_prefix + t.desc_image.url,
                    'social_link': t.social_link,
                    'social_name': t.social_name
                })

            # # More questions?
            # for f in Feedback.objects.all():
            #     self.feedback = f.desc
            self.feedback = self.get_feedback()


            # self.teachers = [t for t in mc.teachers.all()]
            self.list_imgs.clear()
            self.list_imgs = [self.path_prefix + h.file.url for h in
                              PicMasterclass.objects.filter(galleryMasterclass_id=pk)]

            random.shuffle(self.list_imgs)

        except BaseException as e:
            print(e)

        return render(request,
                      self.template_name, {
                          'page': self.page_name,
                          'id'  : self.id,
                          'title': self.title,
                          'desc': self.full_desc,
                          'desc_image': self.desc_image,
                          'teachers': self.teachers,
                          'price': self.price,
                          'list_imgs': self.list_imgs,
                          'video_link': self.video,
                          'who_interested': self.who_i,
                          'list_feedbacks': self.list_feedbacks,
                          'feedback': self.feedback
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
    page = ''
    id_form = ''

    reserve_var = {
        'graduations:reserve': {
            'header': 'Запись на выпускные съёмки',
            'price': '3000',

        },
        'graduations:photoalbum': {
            'header': 'Печать фотоальбома',
            'price': 'от 599'
        },
        'single_masterclass:id': {

        },
        'photoschool:photo': {
            'header': 'Фотография с нуля',
            'price': '12990'
        },
        'studiophoto:studio_photo': {
            'header': 'Основы студийной съёмки',
            'price': '9900'
        }

    }

    def get(self, request):
        self.page = self.request.GET['page']
        self.id_form = self.request.GET['id_form']


        if self.request.is_ajax :
            key = self.page + ':' + self.id_form
            if self.page != 'single_masterclass' and key in self.reserve_var:
                pug = loader.render_to_string('includes/reserved_inc.pug', {
                    'header': self.reserve_var[key]['header'],
                    'price': self.reserve_var[key]['price'],

                })
            else:
                mc = Masterclass.objects.get(pk=self.id_form)

                pug = loader.render_to_string('includes/reserved_inc.pug', {
                    'header': mc.title,
                    'price': mc.price,
                })




        return JsonResponse({'response': 'ok', 'html': pug})

    def post(self, request):
        print("I'm HERE: ", HttpResponse.status_code)
        name = self.request.POST['name']
        phone = self.request.POST['phone']
        email = self.request.POST['email']
        page = self.request.POST['page']
        id_form = self.request.POST['id_form']

        reserve = Reserves()
        reserve.name = name
        reserve.phone = phone
        reserve.email = email
        reserve.page = page

        if page == 'single_masterclass':
            mc = Masterclass.objects.get(pk=id_form)
            reserve.id_form = mc.title
        else:
            reserve.id_form = page

        reserve.save()


        msg_for_admin = EmailMessage(
            subject=u'Новая заявка №' + str(reserve.pk),
            body=u'Получена новая заявка <b>№' + str(reserve.pk) + '</b> '\
            'от <b>' + name + '</b><br>' + \
            'телефон: <b>' + str(phone) + '</b><br>' + \
            'email: <b>' + email + '</b>',
            from_email='atmosphera-sarov@yandex.ru',
            to=(('atmosphera-sarov@yandex.ru'),('Atmospherasarov@yandex.ru')),
            headers={'From': 'atmosphera-sarov@yandex.ru'}
        )

        msg_for_customer = EmailMessage(
            subject=u'Заявка №' + str(reserve.pk) + ' фотостудии Атмосфера',
            body=u'Спасибо, что оставили заяку в нашей фотостудии. Наш администратор \
            свяжется с Вами в ближайшее время.<br>' + \
            'Ваша заявка: <b>№' + str(reserve.pk) + '</b>. <br>'\
            'Вы указали в заявке:<br>' +\
            '    Ваше имя: <b>' + name + '</b><br>' + \
            '    Телефон: <b>' + str(phone) + '</b><br>' + \
            '    email: <b>' + email + '</b>' + \
            '<br><br><br>' + \
            '__________________________________<br>' + \
            'C наилучшими пожеланиями,<br>' +\
            'администрация фотостудии Атмосфера',
            from_email='atmosphera-sarov@yandex.ru',
            to=(email,),
            headers={'From': 'atmosphera-sarov@yandex.ru'}
        )

        msg_for_admin.content_subtype = 'html'
        msg_for_admin.send()

        msg_for_customer.content_subtype = 'html'
        msg_for_customer.send()
        # print(name, phone, email, page, id_form)



        return JsonResponse({'response': HttpResponse.status_code})
        # render(request, 'graduations.pug')


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


# class Feedback(BaseView):
#     title = ''
#     desc = ''
#     last_chance = ''
#
#     def get(self, request):
#         if self.request.is_ajax():
#             try:
#                 # f = [i for i in Feedback.objects.all()]
#                 # self.title = f.title
#                 # self.desc = f.desc
#                 f = Feedback.
#
#             except BaseException as e:
#                 print(e)

# class Reserve(View):
#
#     def post(self, request):
#         print("I'm HERE: ", HttpResponse.status_code)
#         name = self.request.POST['name']
#         phone = self.request.POST['phone']
#         email = self.request.POST['email']
#         page = self.request.POST['page']
#         id_form = self.request.POST['id_form']
#
#         print(name, phone, email, page, id_form)
#
#         return JsonResponse({'response': HttpResponse.status_code})
#         # render(request, 'graduations.pug')

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


# class UsefulChange(View):
#     plate_desc = []
#     pug = ''
#     bb_parser = get_parser()
#     path_prefix = '/static/images/upload_imgs/'
#
#     def get(self, request):
#         self.request.session['view'] = self.request.GET['view']
#         if self.request.is_ajax:
#             self.plate_desc.clear()
#
#             try:
#                 for article in UsefulArticle.objects.all():
#                     self.plate_desc.append({
#                         'image': self.path_prefix + article.desc_image.url,
#                         'header': article.title,
#                         'plate_text': self.bb_parser.render(article.desc)
#                     })
#
#             except BaseException as e:
#                 print(e)
#
#             self.pug = loader.render_to_string('mixins/plate_useful.pug',
#                                                {'plate_desc': self.plate_desc})
#
#         return JsonResponse({'response': 'ok', 'html': self.pug})

# Create your views here.
