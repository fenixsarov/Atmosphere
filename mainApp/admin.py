from django.contrib import admin
from .models import *

from django.shortcuts import get_object_or_404

from multiupload.admin import MultiUploadAdmin



class ImageInlineAdmin(admin.TabularInline):
    # model = Image
    model = Picture


class GalleryMultiuploadMixing(object):

    def process_uploaded_file(self, uploaded, gallery, request):
        if gallery:
            image = gallery.images.create(file=uploaded)
        else:
            image = Picture.objects.create(file=uploaded)
        return {
            'url': image.file.url,
            'thumbnail_url': image.file.url,
            'id': image.id,
            'name': image.filename
        }

class GalleryAdmin(GalleryMultiuploadMixing, MultiUploadAdmin):
    # inlines = [ImageInlineAdmin,]

    multiupload_form = True
    multiupload_list = True

    def delete_file(self, pk, request):
        '''
        Delete an image.
        '''
        obj = get_object_or_404(Picture, pk=pk)
        return obj.delete()


# class ImageAdmin(GalleryMultiuploadMixing, MultiUploadAdmin):
#     multiupload_form = False
#     multiupload_list = True


class PictureAdmin(GalleryMultiuploadMixing, MultiUploadAdmin):
    multiupload_form = True
    multiupload_list = True
    list_display = ['pk', 'filename', 'title']


class MasterclassAdmin(GalleryAdmin):
    multiupload_list = False


class PicMasterclassAdmin(PictureAdmin):
    list_display = ['filename', 'title']


class BlogArticleAdmin(GalleryAdmin):
    list_display = ('title', 'public_date')

    multiupload_list = False


class PicBlogArticleAdmin(PictureAdmin):
    list_display = ['filename', 'title']


class GraduationsAdmin(GalleryAdmin):
    multiupload_list = False


class PicGraduationsAdmin(PictureAdmin):
    list_display = ['filename', 'title']


class UsefulArticleAdmin(admin.ModelAdmin):
    list_display = ['title']


class ProductAdmin(GalleryAdmin):
    multiupload_list = False

    def has_delete_permission(self, request, obj=None):
        return False


class PicProductAdmin(PictureAdmin):
    list_display = ['filename', 'title']


class ReserveAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'public_date', )


class FeedbackAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False


# class CourseBlockProgram(admin.ModelAdmin):
#     list_display = ('name')
#
#
# class CoursePrograms(admin.ModelAdmin):
#     list_display = ('name')

class PhotoCoursesAdmin(GalleryAdmin):
    multiupload_list = False

class PicPhotoCoursesAdmin(PictureAdmin):
    list_display = ['filename', 'title']

# admin.site.register(Gallery, GalleryAdmin)
# admin.site.register(Image, ImageAdmin)
# admin.site.register(Picture, PictureAdmin)
admin.site.register(DescriptionsList)
admin.site.register(Masterclass, MasterclassAdmin)
admin.site.register(PicMasterclass, PicMasterclassAdmin)
admin.site.register(Graduations, GraduationsAdmin)
admin.site.register(PicGraduations, PicGraduationsAdmin)
# admin.site.register(UsefulArticle, UsefulArticleAdmin)
admin.site.register(Hall, ProductAdmin)
admin.site.register(PicHalls, PicProductAdmin)
admin.site.register(Session, ProductAdmin)
admin.site.register(PicSession, PicProductAdmin)
admin.site.register(BlogArticle, BlogArticleAdmin)
admin.site.register(PicBlogArticle, PicBlogArticleAdmin)
# admin.site.register(BlogContentBlock)
admin.site.register(TeamPerson)
admin.site.register(Reserves, ReserveAdmin)
admin.site.register(MasterclassFeedback)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(CourseBlockProgram)
admin.site.register(CoursePrograms)
admin.site.register(PhotoCourses, PhotoCoursesAdmin)
admin.site.register(PicPhotoCourses, PicPhotoCoursesAdmin)
# Register your models here.
