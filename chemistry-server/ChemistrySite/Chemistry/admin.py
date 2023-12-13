from django.contrib import admin

from Chemistry.models import Plant, Substances, Images

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget


# Register your models here.

admin.site.register(Images)

class ImagesAdmin(admin.TabularInline):
    model = Images
    fields = ('plant', 'image')
    # сколько выводимых строк нужно вывести
    extra = 0

class ImagesResource(resources.ModelResource):
    category_plant = fields.Field(column_name="category", attribute="category_plant", widget=ForeignKeyWidget(Substances, 'name'))

    class Meta:
        model = Plant
        #fields = [field.name for field in Plant._meta.fields if field.name != 'id']
        # exclude - поля которые будут исключаться при выгрузке из бд
        #exclude = ['id']


@admin.register(Plant)
class PlantAdmin(ImportExportActionModelAdmin):
    resource_class = ImagesResource
    list_display = ('name', 'category_plant')
    inlines = (ImagesAdmin,)


# class PlantAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category_plant')
#     inlines = (ImagesAdmin,)