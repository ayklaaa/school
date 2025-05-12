from django.contrib import admin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path
from django.utils import timezone
from .models import ContactMessage

from .models import *
from .views import respond_to_message


class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 3


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    inlines = [NewsImageInline]


admin.site.register(Event)
admin.site.register(Teacher)

admin.site.register(Document)
# Register your models here.
admin.site.register(FoodCategory)
# admin.site.register(MenuItem)
# admin.site.register(MenuType)


class MenuDayItemInline(admin.TabularInline):
    model = MenuDayItem
    extra = 1


@admin.register(MenuDay)
class MenuDayAdmin(admin.ModelAdmin):
    inlines = [MenuDayItemInline]
    list_display = ('day', 'date', 'menu_type')
    list_filter = ('day', 'menu_type')


@admin.register(MenuWeek)
class MenuWeekAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')
    filter_horizontal = ('days',)


admin.site.register(FoodMonitoringReport)
admin.site.register(FoodSchedule)
admin.site.register(FoodDocument)


def send_response_email(message):
    subject = f"Ответ на вашу заявку: {message.subject}"
    body = f"""Здравствуйте, {message.name}!

Спасибо за ваше обращение. Вот наш ответ:

{message.admin_response}

С уважением,
Администрация сайта МОУ Размахнинская СОШ"""

    send_mail(
        subject,
        body,
        'filkinajuli@yandex.ru',
        [message.email],
        fail_silently=False,
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'date_sent', 'status')
    list_filter = ('status', 'date_sent')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'date_sent')

    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'subject', 'message', 'date_sent')
        }),
        ('Ответ администратора', {
            'fields': ('status', 'admin_response', 'response_date')
        }),
    )

    def save_model(self, request, obj, form, change):
        if 'admin_response' in form.changed_data and obj.admin_response:
            obj.status = 'completed'
            obj.response_date = timezone.now()
            send_response_email(obj)  # Отправляем email
        super().save_model(request, obj, form, change)