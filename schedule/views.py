from django.shortcuts import render

from schedule.models import *

from django.shortcuts import get_object_or_404

from www.models import Teacher


def schedule(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)
    lessons = Lesson.objects.filter(class_name=class_obj)
    replacements = Replacement.objects.filter(original_lesson__class_name=class_obj)

    context = {
        'class_obj': class_obj,
        'lessons': lessons,
        'replacements': replacements,
    }
    return render(request, 'schedule/schedule.html', context)
# Create your views here.
def class_list(request):
    classes = Class.objects.all()
    return render(request, 'schedule/class_list.html', {'classes': classes})

def teacher_schedule(request):
    teachers = Teacher.objects.prefetch_related('subjects').all()  # Загружаем всех учителей
    teacher_id = request.GET.get('teacher')
    selected_teacher = None
    lessons = []
    replacements = []

    if teacher_id:
        selected_teacher = get_object_or_404(Teacher, id=teacher_id)
        lessons = Lesson.objects.filter(teacher=selected_teacher)
        replacements = Replacement.objects.filter(new_teacher=selected_teacher)

    context = {
        'teachers': teachers,
        'selected_teacher': selected_teacher,
        'lessons': lessons,
        'replacements': replacements,
    }
    return render(request, 'schedule/teacher_schedule.html', context)
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'schedule/teacher_list.html', {'teachers': teachers})