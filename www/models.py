from django.db import models
from django.utils import timezone


class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'

class NewsImage(models.Model):
    article = models.ForeignKey(NewsArticle, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news_images/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.article.title}"

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('academic', 'Academic'),
        ('sports', 'Sports'),
        ('arts', 'Arts'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'События'
        verbose_name_plural = 'События'

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    subjects = models.ManyToManyField("schedule.Subject")
    image = models.ImageField(upload_to='faculty_images/', blank=True)

    # Добавьте эти поля для хранения информации из старой вьюшки
    education = models.TextField(blank=True, verbose_name='Образование')
    experience = models.CharField(max_length=50, blank=True, verbose_name='Опыт работы')
    category = models.CharField(max_length=100, blank=True, verbose_name='Квалификационная категория')
    awards = models.TextField(blank=True, verbose_name='Награды')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')
    reception_hours = models.CharField(max_length=100, blank=True, verbose_name='Часы приема')
    additional = models.TextField(blank=True, verbose_name='Дополнительная информация')

    def __str__(self):
        return self.name

    @property
    def full_name(self):
        return self.name

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'


class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В обработке'),
        ('completed', 'Завершена'),
    ]

    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(max_length=200, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')
    date_sent = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    # Новые поля
    admin_response = models.TextField(blank=True, null=True, verbose_name='Ответ администратора')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )
    response_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата ответа')

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-date_sent']

class Document(models.Model):
    CATEGORY_CHOICES = [
        ('policy', 'Школьная политика'),
        ('form', 'Учителям'),
        ('curriculum', 'Учебный план'),
        ('newsletter', 'Newsletters'),
        ('other', 'Другое'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    upload_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

class FoodCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория питания"
        verbose_name_plural = "Категории питания"


class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    calories = models.IntegerField(default=0)
    proteins = models.FloatField(default=0)
    fats = models.FloatField(default=0)
    carbohydrates = models.FloatField(default=0)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"


class MenuType(models.Model):
    name = models.CharField(max_length=100)  # Например, "Завтрак", "Обед", "Ужин"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип меню"
        verbose_name_plural = "Типы меню"


class MenuDay(models.Model):
    DAY_CHOICES = [
        ('monday', 'Понедельник'),
        ('tuesday', 'Вторник'),
        ('wednesday', 'Среда'),
        ('thursday', 'Четверг'),
        ('friday', 'Пятница'),
        ('saturday', 'Суббота'),
        ('sunday', 'Воскресенье'),
    ]

    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    date = models.DateField(blank=True, null=True)
    menu_type = models.ForeignKey(MenuType, on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem, through='MenuDayItem')

    def __str__(self):
        return f"{self.get_day_display()} - {self.menu_type}"

    class Meta:
        verbose_name = "День меню"
        verbose_name_plural = "Дни меню"


class MenuDayItem(models.Model):
    menu_day = models.ForeignKey(MenuDay, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.menu_day} - {self.menu_item}"

    class Meta:
        ordering = ['order']
        verbose_name = "Элемент дневного меню"
        verbose_name_plural = "Элементы дневного меню"


class MenuWeek(models.Model):
    name = models.CharField(max_length=100)  # Например, "Неделя 1", "Неделя 2"
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    days = models.ManyToManyField(MenuDay, related_name='menu_weeks')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Неделя меню"
        verbose_name_plural = "Недели меню"


class FoodMonitoringReport(models.Model):
    date = models.DateField()
    report_file = models.FileField(upload_to='food_monitoring_reports/')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Отчет о мониторинге питания от {self.date}"

    class Meta:
        verbose_name = "Отчет о мониторинге питания"
        verbose_name_plural = "Отчеты о мониторинге питания"


class FoodSchedule(models.Model):
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.category} ({self.start_time} - {self.end_time})"

    class Meta:
        verbose_name = "Расписание питания"
        verbose_name_plural = "Расписание питания"


class FoodDocument(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='food_documents/')
    upload_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Документ по питанию"
        verbose_name_plural = "Документы по питанию"
from django.db import models

# Create your models here.
