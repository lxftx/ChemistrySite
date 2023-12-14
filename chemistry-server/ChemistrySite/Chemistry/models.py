from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

# Create your models here.

from django.db import models
from modules.services.utils import unique_slugify


class Substances(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Вещество')
    slug = models.SlugField(max_length=255, db_index=True, verbose_name='URL', blank=True)

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plant_list', kwargs={'slug_substances': self.slug})


    class Meta:
        verbose_name = 'Вещество'
        verbose_name_plural = 'Вещества'


class Plant(models.Model):
    name = models.TextField(verbose_name='Название растения')
    slug = models.SlugField(max_length=255, db_index=True, verbose_name='URL', blank=True)
    category_plant = models.ForeignKey(Substances, on_delete=models.CASCADE, verbose_name='Категория вещества', default=None)
    term = models.TextField(verbose_name='Товарное определение', blank=True)
    external_sign = models.TextField(verbose_name='Внешние признаки растения', blank=True)
    distribution = models.TextField(verbose_name='Распространение', blank=True)
    chemical_composition = models.TextField(verbose_name='Химический состав', blank=True)
    harvesting_drying = models.TextField(verbose_name='Сбор, заготовка, сушка', blank=True)
    standardization = models.TextField(verbose_name='Cтандартизация', blank=True)
    microscopy = models.TextField(verbose_name='Микроскопия', blank=True)
    signs = models.TextField(verbose_name='Внешние признаки сырья', blank=True)
    numerical_indicators = models.TextField(verbose_name='Числовые показатели', blank=True)
    keeping = models.TextField(verbose_name='Хранение', blank=True)
    usage = models.TextField(verbose_name='Использование', blank=True)

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Растение'
        verbose_name_plural = 'Растения'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plant', kwargs={'slug_substances': self.category_plant.slug, 'slug_plant': self.slug})



def get_image_filename(instance, filename):
    name = instance.plant.name
    slug = slugify(name)
    return f"post_images/{slug}-{filename}"


class Images(models.Model):
    plant = models.ForeignKey(Plant, default=None, on_delete=models.CASCADE, verbose_name='Название растения')
    image = models.ImageField(upload_to=get_image_filename, null=True, verbose_name='Изображение')

    def __str__(self):
        return self.plant.name

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'


