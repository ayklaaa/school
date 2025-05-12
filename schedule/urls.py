from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from . import views

urlpatterns = [
    path('schedule/<int:class_id>/', views.schedule, name='schedule'),
    path('classes/', views.class_list, name='class_list'),
    path('schedule/<int:class_id>/', views.schedule, name='schedule'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teacher/', views.teacher_schedule, name='teacher_schedule'),
]
