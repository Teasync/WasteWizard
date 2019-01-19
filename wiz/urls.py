from django.urls import path
from . import views

app_name = 'wiz'
urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('all', views.all_items, name='all_items'),
    path('load', views.load, name='load'),
    path('delete', views.delete_all, name='delete')
]