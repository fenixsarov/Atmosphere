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
    # desc = models.TextField(verbose_name='Описание на странице', max_length=256)
    desc = RichTextField(verbose_name='Описание на странице', max_length=2048)
    service_name = models.CharField(verbose_name='Служебное имя', unique=True, max_length=24, default='description')
    prelude = RichTextField(verbose_name='Прелюдия', max_length=13000, blank=True)

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
    # desc = models.TextField(verbose_name='Кракое описание', max_length=2048)
    desc = RichTextField(verbose_name='Кракое описание', max_length=4048)
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


# Эти классы описывают содержание статьи блога
# class BlogContentBlock(models.Model):
#     title = models.CharField('Описание, к какой статье относится', max_length=512)
#     content = RichTextField(verbose_name='Блок контента для статьи блога', max_length=12144)
#     desc_image = models.FileField(upload_to="", verbose_name='Картинка к блоку', blank=True, null=True)
#     def __str__(self):
#         return self.title

#     class Meta:
#         verbose_name_plural = '3.1 Блок статьи блога'

class BlogArticle(models.Model):
    title = models.CharField('Заголовок', max_length=128)
    desc = models.TextField(verbose_name='Краткое описание', max_length=4096)
    desc_image = models.FileField(upload_to="", verbose_name='Картинка к статье')
    # content = models.ManyToManyField(BlogContentBlock, verbose_name='Основной текст')
    content = RichTextField(verbose_name='Блок контента для статьи блога', max_length=12144)

    public_date = models.DateField(verbose_name='Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '3.0 Блог'

class PicBlogArticle(Picture):
    galleryBlogArticle = models.ForeignKey(BlogArticle, related_name='images', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Все изображения со страниц блогов'


#  Этот класс описывает запись об одном из членов команды
class TeamPerson(models.Model):
    title = models.CharField('Имя', max_length=128)
    # desc = models.TextField(verbose_name='Описание', max_length=640)
    desc = RichTextField(verbose_name='Описание', max_length=1280)
    # content = models.TextField(verbose_name='Основной текст')
    content = RichTextField(verbose_name='Основной текст', max_length=1596)
    desc_image = models.FileField(upload_to="", verbose_name='Фотография')
    social_link = models.URLField(verbose_name="Ссылка на социалку")
    social_name = models.URLField(verbose_name="Ссылка на инстаграм")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '4.1 Команда'

# Отзывы к мастерклассам
class MasterclassFeedback(models.Model):
    title = models.CharField(verbose_name='Наименование отзыва', max_length=256)
    name = models.CharField(verbose_name='Имя пользователя', max_length=128)
    image = models.FileField(upload_to="", verbose_name='Фотка/аватарка')
    feedback = models.TextField(verbose_name='Текст отзыва')
    vklink = models.CharField(verbose_name='Ссылка на VK пользователя', max_length=256)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '6.0 Отзывы к мастерклассам'


# Эти два класса описывают изображения на странице мастерклассов и само содежимое каждого мастеркласса
class Masterclass(models.Model):
    title = models.CharField('Название мастер-класса', max_length=128)
    # teacher = models.ForeignKey(TeamPerson,  blank=False, null=False)
    teachers = models.ManyToManyField(TeamPerson,  blank=False)
    price = models.IntegerField(verbose_name='Стоимость', default=1500)
    # num_of_place = models.IntegerField(verbose_name='Количество мест', default=10)
    short_desc = RichTextField(verbose_name='Кракое описание мастер-класса', max_length=640)
    full_desc = RichTextField(verbose_name='Полное описание мастер-класса', max_length=3072)
    desc_image = models.FileField(upload_to="", verbose_name='Титульное изображение')
    who_interested = RichTextField(verbose_name='Кому интересен мастер-класс', max_length=8096, blank=True)
    video = EmbedVideoField(verbose_name='Ссылка на видео', blank=True, default='')
    # service_name = models.CharField(verbose_name='Служебное имя', max_length=24, default='masterclass_name')
    feedback = models.ManyToManyField(MasterclassFeedback, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '2.2 Мастерклассы'


class PicMasterclass(Picture):
    galleryMasterclass = models.ForeignKey(Masterclass, related_name='images', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Все изображения со страницы мастерклассов'


class Reserves(models.Model):
    name = models.CharField(verbose_name='Имя заказчика', max_length=256)
    email = models.EmailField(verbose_name='email закачика', max_length=256)
    phone = models.CharField(verbose_name='Телефон', max_length=11)
    page = models.CharField(verbose_name='Страница, откуда пришла заявка', max_length=64)
    id_form = models.CharField(verbose_name='id_form', max_length=64 )
    public_date = models.DateField(auto_now_add=True, verbose_name='Дата создания заявки')

    def __str__(self):
        return 'Заявка № {} от {}, дата заявки {}'.format(self.pk ,self.name, self.public_date.isoformat())

    class Meta:
        verbose_name_plural = '5.0 Заявки'


class Feedback(models.Model):
    # title = models.CharField(verbose_name='Имя заказчика', max_length=64, default='Остались вопросы?')
    desc = RichTextField(verbose_name='Центральный блок текста', max_length=4096)

    def __str__(self):
        return 'Остались вопросы?'

    class Meta:
        verbose_name_plural = '7.0 Feedback (остались вопросы?)'

# Класс модели данных фотографии с нуля в разделе фотошколы
class CourseBlockProgram(models.Model):
    intro = RichTextField(verbose_name='Вступление перед блоком', max_length=4096)
    title = models.CharField('Название блока', max_length=128)
    desc = RichTextField(verbose_name='Описание блока', max_length=4096)
    teacher = models.ManyToManyField(TeamPerson,  blank=False)
    desc_image = models.FileField(upload_to="", verbose_name='Картинка блока')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '2.1.1 Описание блоков курсов фотошколы'

class CoursePrograms(models.Model):
    title = models.CharField('Название программы курса', max_length=128)
    course = models.ManyToManyField(CourseBlockProgram, blank=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '2.1.0 Содержание курсов фотошколы'

class PhotoFromScratch(models.Model):
    title = models.CharField('Название курса', max_length=128)
    short_desc = RichTextField(verbose_name='Кракое описание курса', max_length=640)
    full_desc = RichTextField(verbose_name='Полное описание курса', max_length=3072)
    desc_image = models.FileField(upload_to="", verbose_name='Титульное изображение')
    price = models.IntegerField(verbose_name="Стоимость курса", default=12900)
    who_interested = RichTextField(verbose_name='Кому интересен курс', max_length=8096, blank=True)
    teachers = models.ManyToManyField(TeamPerson,  blank=False)

    # Программа курса
    course_program = models.OneToOneField(CoursePrograms, blank=False)

    constructor = RichTextField(verbose_name="Конструктор")
    start_date = models.DateField(verbose_name="Дата ближайшего набора на курс", auto_now_add=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '2.1 Фотошкола'


class PicPhotoFromScratch(Picture):
    galleryMasterclass = models.ForeignKey(
        PhotoFromScratch, related_name='images', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Все изображения курсов фотошколы'
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
