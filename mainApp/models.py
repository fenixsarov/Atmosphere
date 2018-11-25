from django.db import models
from django import forms
from ckeditor.fields import RichTextField
from embed_video.fields import EmbedVideoField
from precise_bbcode.fields import BBCodeTextField
# Create your models here.

# Two abstract classes for saving and grouping images
class Gallery(models.Model):
    title = models.CharField('Title', max_length=20)
    desc = models.TextField(verbose_name='Описание на странице', max_length=256)
    service_name = models.CharField(verbose_name='Служебное имя', unique=True, max_length=24, default='gallery')

    def __str__(self):
        return self.title

    # class Meta:
    #     abstract = True


class Picture(models.Model):
    # gallery = models.ForeignKey(Gallery, related_name='images', blank=True, null=True)
    title = models.CharField(verbose_name="Название картинки", max_length=32)
    file = models.FileField(upload_to="")
    desc = models.TextField(verbose_name='Описание изображения', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.filename

    # class Meta:
        # verbose_name = "Изображения"
        # verbose_name_plural = "Все изображения"
        # abstract = True

    @property
    def filename(self):
        return self.file.name.rsplit('/', 1)[-1]


# Эти два класса описывают изображения на странице выпускных съёмок и само содежимое каждого из них
class Graduations(models.Model):
    title = models.CharField('Title', max_length=128)
    price = models.IntegerField(verbose_name='Стоимость', default=1500)
    desc = models.TextField(verbose_name='Кракое описание', max_length=256)
    service_name = models.CharField(verbose_name='Служебное имя', unique=True, max_length=24, default='graduations_name')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '1.3 Выпускные съёмки'


class PicGraduations(Picture):
    galleryGraduations = models.ForeignKey(Graduations, related_name='images', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Все изображения со страницы выпускных съёмок'


# Этот класс описывает верхние части страниц, где есть описание и фотография контекста
class DescriptionsList(models.Model):
    title = models.CharField('Title', max_length=30)
    file = models.FileField(upload_to="")
    desc = models.TextField(verbose_name='Описание на странице', max_length=256)
    service_name = models.CharField(verbose_name='Служебное имя', unique=True, max_length=24, default='description')

    class Meta:
        verbose_name_plural = '0. Список описаний страниц'

    def __str__(self):
        return self.title


# Models for describe article on useful page
# class UsefulArticle(models.Model):
#     title = models.CharField('Title', max_length=30)
#     desc = models.TextField(verbose_name='Описание статьи', max_length=256)
#     desc_image = models.FileField(upload_to="", verbose_name='Картинка к статье')
#     service_name = models.CharField(verbose_name='Служебное имя', unique=True, max_length=24, default='article')
#
#     class Meta:
#         verbose_name_plural = '2.3 Статьи на странице "Полезное"'
#
#     def __str__(self):
#         return self.title


# Models for halls and sessions
class Product(models.Model):
    title = models.CharField('Заголовок', max_length=128)
    desc = models.TextField(verbose_name='Кракое описание', max_length=256)
    service_name = models.CharField(verbose_name='Служебное имя', unique=True, max_length=24,
                                    default='product')

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Hall(Product):
    hall_size = models.IntegerField(verbose_name='Размер зала', default=50)
    price = models.IntegerField(verbose_name='Стоимость', default=1500)

    class Meta(Product.Meta):
        verbose_name_plural = '1.2 Залы'


class PicHalls(Picture):
    galleryHalls = models.ForeignKey(Hall, related_name='images', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Все изображения залов'


class Session(Product):
    class Meta(Product.Meta):
        verbose_name_plural = '1.1 Съёмки'


class PicSession(Picture):
    gallerySession = models.ForeignKey(Session, related_name='images', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Все изображения съёмок'


# Этот класс описывает содержание статьи блога
class BlogArticle(models.Model):
    title = models.CharField('Заголовок', max_length=128)
    desc = models.TextField(verbose_name='Описание', max_length=256)
    desc_image = models.FileField(upload_to="", verbose_name='Картинка к статье')
    content = models.TextField(verbose_name='Основной текст')
    public_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '3.0 Блог'


#  Этот класс описывает запись об одном из членов команды
class TeamPerson(models.Model):
    title = models.CharField('Имя', max_length=128)
    desc = models.TextField(verbose_name='Описание', max_length=256)
    content = models.TextField(verbose_name='Основной текст')
    desc_image = models.FileField(upload_to="", verbose_name='Фотография')
    social_link = models.URLField(verbose_name="Ссылка на социалку")
    social_name = models.URLField(verbose_name="Ссылка на инстаграм")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '4.1 Команда'


# Эти два класса описывают изображения на странице мастерклассов и само содежимое каждого мастеркласса
class Masterclass(models.Model):
    title = models.CharField('Название мастер-класса', max_length=128)
    # teacher = models.ForeignKey(TeamPerson,  blank=False, null=False)
    teachers = models.ManyToManyField(TeamPerson,  blank=False)
    price = models.IntegerField(verbose_name='Стоимость', default=1500)
    # num_of_place = models.IntegerField(verbose_name='Количество мест', default=10)
    short_desc = RichTextField(verbose_name='Кракое описание мастер-класса', max_length=640)
    full_desc = RichTextField(verbose_name='Полное описание мастер-класса', max_length=2048)
    desc_image = models.FileField(upload_to="", verbose_name='Титульное изображение')
    video = EmbedVideoField(verbose_name='Ссылка на видео', blank=False)
    # service_name = models.CharField(verbose_name='Служебное имя', max_length=24, default='masterclass_name')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '2.2 Мастерклассы'


class PicMasterclass(Picture):
    galleryMasterclass = models.ForeignKey(Masterclass, related_name='images', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Все изображения со страницы мастерклассов'

# class Image(models.Model):
#     file = models.FileField('File', upload_to='static/images/upload_imgs/')
#     gallery = models.ForeignKey('Gallery', related_name='images', blank=True, null=True)
#
#     def __str__(self):
#         return self.filename
#
#     @property
#     def filename(self):
#         return self.file.name.rsplit('/', 1)[-1]