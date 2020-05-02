#from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path, include
from . import views 

app_name = 'expense'

urlpatterns = [
    path('post_create/',views.post_create, name="post_create"),
    path('post_detail/<int:id>',views.post_detail, name="post_detail"),   
    path('timeline/',views.timeline, name="timeline"),
    path('post_update/<int:id>',views.post_update, name="post_update"),
    path('post_delete/<int:id>',views.post_delete, name="post_delete"),
    path('analytics/',views.analytics,name='analytics'),
    path('budget/',views.budget,name='budget'),
    path('calendar/<str:date>/<str:month>/<str:year>',views.calendar,name='calendar'),
    path('calendarToday/',views.calendarToday,name='calendarToday'),
]
