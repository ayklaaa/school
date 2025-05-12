from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .views import *
urlpatterns = [
    path('my/admin-panel', admin_panel, name='admin_panel'),
]