from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
        path('', home, name='home'),
        path('contact/', contact, name='contact'),
        path('documents/', documents, name='documents'),
        path('news/', NewsListView.as_view(), name='news'),
        path('news/<int:pk>/', news_details.as_view(), name='news_details'),
        path('info/', school_info, name='info'),
        path('svedeniya/', organization_info, name='organization_info'),
        path('structure', structure, name='structure'),
        path('education', education, name='education'),
        path('standart', standart, name='standart'),
        path('material_support', material_support, name='material_support'),
        path('financial', financial, name='financial'),
        path('first-grade-admission/', first_grade_admission, name='first_grade_admission'),
        path('clubs-and-sections/', clubs_and_sections, name='clubs_and_sections'),
        path('rucovodstvo/', staff, name='staff'),
        path('vospitatelnaya-rabota/', educational_work, name='educational_work'),
        path('food-monitoring/', food_monitoring, name='food_monitoring'),
        path('quality-assessment/', quality_assessment, name='quality_assessment'),
        path('scholarships/', scholarships, name='scholarships'),
        path('paid-services/', paid_services, name='paid_services'),
        path('international/', international, name='international'),
        path('vacant', vacant_places, name='vacant'),
        path('local-acts/', local_acts, name='local_acts'),
        path('contactmessage/<int:pk>/respond/', respond_to_message, name='respond_to_message'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
