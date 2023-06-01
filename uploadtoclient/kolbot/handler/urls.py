from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('kolesafilters/', views.kolesafilters, name='kolesafilters'),
    path('kolesaclients/', views.kolesaclients, name='kolesaclients'),
    path('updatelastcar/', views.updatelastcar, name='updatelastcar')
]
