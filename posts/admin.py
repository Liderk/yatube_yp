from django.contrib import admin
from .models import Post, Group


# admin.site.register(Post)

class PostAdmin(admin.ModelAdmin):
    # перечисляем поля, которые должны отображаться в админке
    list_display = ("pk", "text", "pub_date", "author")
    # добавляем интерфейс для поиска по тексту постов
    search_fields = ("text",)
    # добавляем возможность фильтрации по дате
    list_filter = ("pub_date",)
    # это свойство сработает для всех колонок: где пусто - там будет эта строка
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    # перечисляем поля, которые должны отображаться в админке
    list_display = ("pk", "title", "description")
    # добавляем интерфейс для отображения парамтеров групп
    search_fields = ("title",)
    list_filter = ("title",)
    empty_value_display = '-пусто-'


# при регистрации модели Post и источником конфигурации для них назначаем класс PostAdmin и GroupAdmin
admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
