from django.contrib import admin
from .models import Article

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'title', 'content', 'image', 'created_date')
    list_display_links = ('id', 'slug', 'title')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Article, ArticleAdmin)
