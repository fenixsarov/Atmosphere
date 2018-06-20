from django.db import models
from django import forms


# Create your models here.

class SchoolImgs(models.Model):
    name = models.CharField(verbose_name="Название картинки", max_length=32, unique=True)
    # image = models.FilePathField(path="static/images/school")
    image = models.FileField(upload_to="static/images/school")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Основные изображения на странице 'Фотошколы'"


class Gallery(models.Model):
    class Meta:
        verbose_name_plural = 'Galleries'
    title = models.CharField('Title', max_length=20)
    desc = models.TextField(verbose_name='Описание на странице', max_length=256)

    def __str__(self):
        return self.title


class Image(models.Model):
    file = models.FileField('File', upload_to='static/images/school/')
    gallery = models.ForeignKey('Gallery', related_name='images', blank=True, null=True)

    def __str__(self):
        return self.filename

    @property
    def filename(self):
        return self.file.name.rsplit('/', 1)[-1]