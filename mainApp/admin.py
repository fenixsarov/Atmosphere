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


# admin.site.register(Gallery, GalleryAdmin)
# admin.site.register(Image, ImageAdmin)
# admin.site.register(Picture, PictureAdmin)
admin.site.register(DescriptionsList)
admin.site.register(Masterclass, MasterclassAdmin)
admin.site.register(PicMasterclass, PicMasterclassAdmin)
admin.site.register(Graduations, GraduationsAdmin)
admin.site.register(PicGraduations, PicGraduationsAdmin)
admin.site.register(UsefulArticle, UsefulArticleAdmin)
admin.site.register(Hall, ProductAdmin)
admin.site.register(PicHalls, PicProductAdmin)
admin.site.register(Session, ProductAdmin)
admin.site.register(PicSession, PicProductAdmin)
# Register your models here.
