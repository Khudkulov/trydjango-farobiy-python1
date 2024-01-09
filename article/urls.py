from django.urls import path
from .views import (
    article_detail,
    article_list,
    article_create,
    article_creat_form,
    article_change,
    article_delete
)


app_name = 'article'

urlpatterns = [
    path('', article_list, name='list'),
    path('index/<slug:slug>', article_detail, name='detail'),
    path('article/create/', article_create, name='create'),
    path('article/create/form/', article_creat_form, name='create-form'),
    path('article/change/<slug:slug>', article_change, name='change-form'),
    path('article/delete/<slug:slug>', article_delete, name='delete'),
]
