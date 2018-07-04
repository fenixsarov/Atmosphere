from django.db import models
from django import forms


# Create your models here.

class Gallery(models.Model):
    title = models.CharField('Title', max_length=20)
    desc = models.TextField(verbose_name='Описание на странице', max_length=256)
    service_name = models.CharField(verbose_name='Служебное имя', unique=True, max_length=24, default='gallery')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Галереи изображений'

class Picture(models.Model):
    gallery = models.ForeignKey(Gallery, related_name='images', blank=True, null=True)
    title = models.CharField(verbose_name="Название картинки", max_length=32)
    file = models.FileField(upload_to="static/images/school")
    desc = models.TextField(verbose_name='Описание изображения', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.filename

    class Meta:
        # verbose_name = "Изображения"
        verbose_name_plural = "Все изображения"

    @property
    def filename(self):
        return self.file.name.rsplit('/', 1)[-1]


# Эти два класса описывают изображения на странице мастерклассов и само содежимое каждого мастеркласса
class Masterclass(models.Model):
    title = models.CharField('Title', max_length=128)
    teacher = models.CharField(verbose_name='Преподаватель', max_length=32)
    price = models.IntegerField(verbose_name='Стоимость', default=1500)
    num_of_place = models.IntegerField(verbose_name='Количество мест', default=10)
    short_desc = models.TextField(verbose_name='Кракое описание мастер-класса', max_length=256)
    full_desc = models.TextField(verbose_name='Полное описание мастер-класса', max_length=512)
    desc_image = models.FileField(upload_to="static/images/school", verbose_name='Титульное изображение')
    # service_name = models.CharField(verbose_name='Служебное имя', max_length=24, default='masterclass_name')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Мастерклассы'


class PicMasterclass(Picture):
    galleryMasterclass = models.ForeignKey(Masterclass, related_name='images', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Все изображения со страницы мастерклассов'


# Эти два класса описывают изображения на странице выпускных съёмок и само содежимое каждого из них
class Graduations(models.Model):
    title = models.CharField('Title', max_length=128)
    price = models.IntegerField(verbose_name='Стоимость', default=1500)
    desc = models.TextField(verbose_name='Кракое описание', max_length=256)
    service_name = models.CharField(verbose_name='Служебное имя', unique=True, max_length=24, default='graduations_name')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Выпускные съёмки'


class PicGraduations(Picture):
    galleryGraduations = models.ForeignKey(Graduations, related_name='images', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Все изображения со страницы выпускных съёмок'



class DescriptionsList(models.Model):
    title = models.CharField('Title', max_length=20)
    file = models.FileField(upload_to="static/images/school")
    desc = models.TextField(verbose_name='Описание на странице', max_length=256)
    service_name = models.CharField(verbose_name='Служебное имя', unique=True, max_length=24, default='description')

    class Meta:
        verbose_name_plural = 'Список описаний страниц'

    def __str__(self):
        return self.title




# class Image(models.Model):
#     file = models.FileField('File', upload_to='static/images/school/')
#     gallery = models.ForeignKey('Gallery', related_name='images', blank=True, null=True)
#
#     def __str__(self):
#         return self.filename
#
#     @property
#     def filename(self):
#         return self.file.name.rsplit('/', 1)[-1]