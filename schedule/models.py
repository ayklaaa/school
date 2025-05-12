from django.db import models
from django.core.exceptions import ValidationError


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

class Classroom(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Учебный кабинет'
        verbose_name_plural = 'Учебные кабинеты'
class Class(models.Model):
    name = models.CharField(max_length=50)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Номер класса'
        verbose_name_plural = 'Номер класса'

class Lesson(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    teacher = models.ForeignKey('www.Teacher', on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey('schedule.Subject', on_delete=models.SET_NULL, null=True)
    day_of_week = models.CharField(max_length=10, choices=[
        ('Monday', 'Понедельник'),
        ('Tuesday', 'Вторник'),
        ('Wednesday', 'Среда'),
        ('Thursday', 'Четверг'),
        ('Friday', 'Пятница'),
        ('Saturday', 'Суббота'),
    ])
    lesson_number = models.IntegerField()  # Номер урока (1, 2, 3, ...)

    def clean(self):
        # Проверка на повторение уроков у одного класса в один день
        existing_lessons = Lesson.objects.filter(
            class_name=self.class_name,
            day_of_week=self.day_of_week,
            lesson_number=self.lesson_number,
        ).exclude(id=self.id)  # Исключаем текущий урок при редактировании

        if existing_lessons.exists():
            raise ValidationError(
                f"У класса {self.class_name} уже есть урок в {self.day_of_week} на {self.lesson_number} урок."
            )

        # Проверка на то, что учитель не ведёт урок одновременно в двух классах
        teacher_conflict = Lesson.objects.filter(
            teacher=self.teacher,
            day_of_week=self.day_of_week,
            lesson_number=self.lesson_number,
        ).exclude(id=self.id)

        if teacher_conflict.exists():
            raise ValidationError(
                f"Учитель {self.teacher} уже ведёт урок в {self.day_of_week} на {self.lesson_number} урок."
            )

        # Проверка на то, что кабинет не занят другим классом
        if self.class_name.classroom:
            classroom_conflict = Lesson.objects.filter(
                class_name__classroom=self.class_name.classroom,
                day_of_week=self.day_of_week,
                lesson_number=self.lesson_number,
            ).exclude(id=self.id)

            if classroom_conflict.exists():
                raise ValidationError(
                    f"Кабинет {self.class_name.classroom} уже занят в {self.day_of_week} на {self.lesson_number} урок."
                )

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызов проверок перед сохранением
        super().save(*args, **kwargs)

    def __str__(self):
            return f"{self.class_name} - {self.subject} ({self.teacher})"

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'
class Replacement(models.Model):
    original_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    new_teacher = models.ForeignKey('www.Teacher', on_delete=models.CASCADE, null=True, blank=True)
    new_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()  # Дата замены

    def __str__(self):
        return f"Замена для {self.original_lesson} на {self.date}"

    class Meta:
        verbose_name = 'Замена'
        verbose_name_plural = 'Замена'

# Create your models here.
