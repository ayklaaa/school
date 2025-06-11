from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView

from .models import *
from .forms import ContactForm, ContactMessageResponseForm
from django import forms
from .models import ContactMessage
from .utils import send_response_email
def home(request):
    news_articles = NewsArticle.objects.order_by('-date_posted')[:6]  # Загружаем больше новостей
    upcoming_events = Event.objects.all().order_by('-date')[:4]
    faculty_members = Teacher.objects.all()[:4]

    context = {
        'news_articles': news_articles,
        'upcoming_events': upcoming_events,
        'faculty_members': faculty_members,
    }
    return render(request, 'home.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваше обращение отправленно. Спасибо!')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})



def documents(request):
    documents = Document.objects.all().order_by('-upload_date')
    categories = Document.CATEGORY_CHOICES

    context = {
        'documents': documents,
        'categories': categories,
    }
    return render(request, 'documents.html', context)


# Create your views here.
class NewsListView(ListView):
    model = NewsArticle
    template_name = 'news.html'
    context_object_name = 'news_articles'

class news_details(DetailView):
    model = NewsArticle
    template_name = 'news_detail.html'
    context_object_name = 'article'

def school_info(request):
    school_data = {
        'foundation_date': '1964',
        'short_name': 'МОУ Размахнинская СОШ',
        'full_name': 'МУНИЦИПАЛЬНОЕ ОБЩЕОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ РАЗМАХНИНСКАЯ СРЕДНЯЯ ОБЩЕОБРАЗОВАТЕЛЬНАЯ ШКОЛА',
    }
    return render(request, 'info.html', {'school_data': school_data})


def organization_info(request):
    return render(request, 'organization_info.html')


def structure(request):
    return render(request, 'structure.html')


def education(request):
    return render(request, 'education.html')


def standart(request):
    return render(request, 'standart.html')


def material_support(request):
    return render(request, 'material_support.html')


def financial(request):
    return render(request, 'financial.html')


def first_grade_admission(request):
    # Информация о наборе в первый класс
    admission_info = {
        'start_date': '1 февраля 2024 года',
        'end_date': '30 июня 2024 года',
        'second_wave_start': '6 июля 2024 года',
        'second_wave_end': '5 сентября 2024 года',
        'contact_person': 'Иванова Елена Петровна',
        'contact_phone': '8 30 (244) 31-5-11',
        'contact_email': 'admission@razmahnino-sosh.ru',
        'school_year': '2024-2025',
        'planned_classes': 2,
        'planned_students': 50,
    }

    # Список необходимых документов
    required_documents = [
        'Заявление о приеме на обучение',
        'Копия документа, удостоверяющего личность родителя (законного представителя)',
        'Копия свидетельства о рождении ребенка',
        'Копия документа о регистрации ребенка по месту жительства',
        'Справка с места работы родителя(ей) (при наличии права внеочередного или первоочередного приема)',
        'Копия заключения психолого-медико-педагогической комиссии (при наличии)',
    ]

    # Часто задаваемые вопросы
    faq = [
        {
            'question': 'Когда начинается прием заявлений в первый класс?',
            'answer': 'Прием заявлений в первый класс для детей, проживающих на закрепленной территории, начинается 1 февраля и завершается 30 июня текущего года. Для детей, не проживающих на закрепленной территории, прием заявлений начинается с 6 июля до момента заполнения свободных мест, но не позднее 5 сентября текущего года.'
        },
        {
            'question': 'Какие документы необходимы для поступления в первый класс?',
            'answer': 'Для поступления в первый класс необходимы следующие документы: заявление о приеме, копия документа, удостоверяющего личность родителя, копия свидетельства о рождении ребенка, копия документа о регистрации ребенка по месту жительства, справка с места работы родителя(ей) (при наличии права внеочередного или первоочередного приема), копия заключения психолого-медико-педагогической комиссии (при наличии).'
        },
        {
            'question': 'Как подать заявление о приеме в первый класс?',
            'answer': 'Заявление о приеме в первый класс можно подать несколькими способами: лично в школе, через операторов почтовой связи заказным письмом с уведомлением о вручении, в электронной форме через электронную почту школы или через портал Госуслуги.'
        },
        {
            'question': 'Какой возраст должен быть у ребенка для поступления в первый класс?',
            'answer': 'В первый класс принимаются дети, достигшие к 1 сентября текущего года возраста не менее 6 лет и 6 месяцев, но не старше 8 лет. По заявлению родителей (законных представителей) учредитель образовательной организации может разрешить прием детей в более раннем или более позднем возрасте.'
        },
        {
            'question': 'Есть ли преимущественное право при зачислении в первый класс?',
            'answer': 'Да, преимущественное право зачисления на обучение по основным общеобразовательным программам начального общего образования имеют дети, проживающие в одной семье и имеющие общее место жительства, если в школе уже обучаются их братья и (или) сестры. Также существуют категории граждан, имеющих право на внеочередное или первоочередное предоставление места в школе в соответствии с законодательством РФ.'
        },
    ]

    # Советы для родителей будущих первоклассников
    tips = [
        {
            'title': 'Развивайте самостоятельность',
            'content': 'Приучайте ребенка к самостоятельности в бытовых действиях и самообслуживании. Ребенок должен уметь самостоятельно одеваться, переобуваться, завязывать шнурки, собирать портфель, убирать за собой вещи и игрушки.',

        },
        {
            'title': 'Развивайте речь',
            'content': 'Следите за правильностью речи ребенка. Читайте книги, обсуждайте прочитанное, учите стихи наизусть, поощряйте ребенка высказывать свои мысли и суждения.',

        },
        {
            'title': 'Тренируйте мелкую моторику',
            'content': 'Развивайте мелкую моторику рук. Это можно делать с помощью лепки, рисования, аппликации, конструирования, собирания мозаики и пазлов.',

        },
        {
            'title': 'Учите общаться',
            'content': 'Помогайте ребенку в развитии навыков общения. Учите его знакомиться с другими детьми, обращаться к ним по имени, просить, а не отнимать игрушки, предлагать свои игрушки другим детям.',

        },
        {
            'title': 'Соблюдайте режим дня',
            'content': 'Постепенно приучайте ребенка к режиму дня, близкому к школьному. Это поможет ему легче адаптироваться к новому распорядку.',

        },
        {
            'title': 'Формируйте познавательный интерес',
            'content': 'Поддерживайте интерес ребенка к обучению и познанию нового. Хвалите его за успехи и достижения, не ругайте за ошибки и неудачи.',

        },
    ]

    context = {
        'admission_info': admission_info,
        'required_documents': required_documents,
        'faq': faq,
        'tips': tips,
    }

    return render(request, 'parens/first_grade_admission.html', context)


def clubs_and_sections(request):
    # Категории кружков и секций
    categories = [
        {'id': 'sports', 'name': 'Спортивные секции'},

    ]

    # Получаем выбранную категорию из параметра запроса или используем первую категорию по умолчанию
    selected_category_id = request.GET.get('category', 'sports')
    selected_category = next((c for c in categories if c['id'] == selected_category_id), categories[0])

    # Кружки и секции
    clubs = [
        {
            'id': 'volleyball',
            'name': 'Волейбол',
            'category': 'sports',
            'description': 'Секция волейбола для учащихся 5-11 классов. Тренировки направлены на развитие физических качеств, обучение технике и тактике игры, формирование командного духа.',
            'instructor': 'Морозов Дмитрий Иванович',
            'schedule': 'Понедельник, среда, пятница: 15:00 - 16:30',
            'location': 'Спортивный зал',
            'age': '11-17 лет',
            'achievements': [
                'Победители районных соревнований 2022 года',
                'Призеры областных соревнований 2023 года',
            ],
            'image': 'images/volleyball.jpg',
        },
        {
            'id': 'basketball',
            'name': 'Баскетбол',
            'category': 'sports',
            'description': 'Секция баскетбола для учащихся 5-11 классов. Занятия включают общую физическую подготовку, обучение технике игры, тактические приемы, участие в соревнованиях.',
            'instructor': 'Морозов Дмитрий Иванович',
            'schedule': 'Вторник, четверг: 15:00 - 16:30, суббота: 10:00 - 11:30',
            'location': 'Спортивный зал',
            'age': '11-17 лет',
            'achievements': [
                'Призеры районных соревнований 2023 года',
            ],
            'image': 'images/basketball.jpg',
        },
    ]

    # Фильтруем кружки по выбранной категории
    filtered_clubs = [club for club in clubs if club['category'] == selected_category_id]

    # Информация о записи в кружки и секции
    enrollment_info = {
        'start_date': '1 сентября 2023 года',
        'end_date': '15 сентября 2023 года',
        'contact_person': 'Сидорова Мария Владимировна',
        'contact_phone': '8 30 (244) 31-5-11',
        'contact_email': 'clubs@razmahnino-sosh.ru',
        'requirements': [
            'Заявление от родителей (законных представителей)',
            'Медицинская справка (для спортивных секций)',
            'Согласие на обработку персональных данных',
        ],
    }

    # Часто задаваемые вопросы
    faq = [
        {
            'question': 'Как записаться в кружок или секцию?',
            'answer': 'Для записи в кружок или секцию необходимо подать заявление от родителей (законных представителей) руководителю кружка или в администрацию школы. Для спортивных секций также требуется медицинская справка о состоянии здоровья ребенка.'
        },
        {
            'question': 'Сколько кружков может посещать один ученик?',
            'answer': 'Ученик может посещать несколько кружков и секций, но рекомендуется выбирать не более 2-3, чтобы не перегружать ребенка и оставлять время на выполнение домашних заданий и отдых.'
        },
        {
            'question': 'Нужно ли платить за занятия в кружках и секциях?',
            'answer': 'Большинство кружков и секций в нашей школе бесплатные, так как финансируются из бюджетных средств. Некоторые специализированные кружки могут быть платными, информация о стоимости предоставляется при записи.'
        },
        {
            'question': 'Могут ли посещать кружки и секции дети, не обучающиеся в школе?',
            'answer': 'В первую очередь в кружки и секции зачисляются учащиеся нашей школы. При наличии свободных мест могут быть зачислены дети, не обучающиеся в нашей школе, но проживающие в микрорайоне.'
        },
        {
            'question': 'Что делать, если ребенок хочет сменить кружок или секцию?',
            'answer': 'Если ребенок хочет сменить кружок или секцию, родителям необходимо написать заявление об отчислении из текущего кружка и заявление о зачислении в новый кружок. Рекомендуется обсудить это решение с руководителями кружков и классным руководителем.'
        },
    ]

    context = {
        'categories': categories,
        'selected_category': selected_category,
        'clubs': filtered_clubs,
        'enrollment_info': enrollment_info,
        'faq': faq,
    }

    return render(request, 'parens/clubs_and_sections.html', context)


def staff(request):
    # Получаем всех учителей из базы данных
    all_teachers = Teacher.objects.all().prefetch_related('subjects')

    # Данные о руководстве школы (можно выделить по должности)
    leadership = all_teachers.filter(
        position__in=['Директор', 'Заместитель директора по учебно-воспитательной работе',
                      'Заместитель директора по воспитательной работе',
                      'Заместитель директора по административно-хозяйственной части']
    )

    # Категории педагогов для фильтрации
    categories = [
        {'id': 'all', 'name': 'Учителя'},
        {'id': 'leadership', 'name': 'Руководство'},
        {'id': 'primary', 'name': 'Нач. классы'},
        {'id': 'humanities', 'name': 'Гуманитарные'},
        {'id': 'science', 'name': 'Естественные науки'},
        {'id': 'arts', 'name': 'Эстет. цикл'},
        {'id': 'support', 'name': 'Пед. сопровождение'},
    ]

    # Получаем выбранную категорию из параметра запроса
    selected_category_id = request.GET.get('category', 'all')
    selected_category = next((c for c in categories if c['id'] == selected_category_id), categories[0])

    # Фильтруем педагогов по выбранной категории
    if selected_category_id == 'all':
        filtered_teachers = all_teachers.exclude(id__in=leadership.values_list('id', flat=True))
    elif selected_category_id == 'leadership':
        filtered_teachers = leadership
    elif selected_category_id == 'primary':

        filtered_teachers = all_teachers.filter(position__icontains='начал')  # Исправлен синтаксис

    elif selected_category_id == 'humanities':
        humanities_subjects = ['русск', 'литератур', 'истори', 'обществознан', 'английск']
        filtered_teachers = all_teachers.filter(
            subjects__name__iregex=r'(' + '|'.join(humanities_subjects) + ')'
        ).distinct()
    elif selected_category_id == 'science':
        science_subjects = ['математ', 'Матем', 'физик', 'информатик', 'хими', 'биологи', 'географи']
        filtered_teachers = all_teachers.filter(
            subjects__name__iregex=r'(' + '|'.join(science_subjects) + ')'
        ).distinct()
    elif selected_category_id == 'arts':
        arts_subjects = ['музык', 'изобразительн', 'технолог', 'физкультур']
        filtered_teachers = all_teachers.filter(
            subjects__name__iregex=r'(' + '|'.join(arts_subjects) + ')'
        ).distinct()
    elif selected_category_id == 'support':
        support_positions = ['психолог', 'социальный педагог', 'библиотекарь']
        filtered_teachers = all_teachers.filter(
            position__iregex=r'(' + '|'.join(support_positions) + ')'
        )
    else:
        filtered_teachers = all_teachers.none()

    # Статистика педагогического состава (примерная, нужно адаптировать под ваши данные)
    stats = {
        'total_teachers': all_teachers.count(),
        'higher_education': all_teachers.count(),  # Предполагаем, что все с высшим образованием
        # Остальные статистические данные нужно будет добавить в модель Teacher
    }

    context = {
        'leadership': leadership,
        'teachers': filtered_teachers,
        'stats': stats,
        'categories': categories,
        'selected_category': selected_category,
    }

    return render(request, 'staff.html', context)


def educational_work(request):
    # Основные направления воспитательной работы
    directions = [
        {
            'title': 'Гражданско-патриотическое воспитание',
            'description': 'Формирование гражданской идентичности, патриотизма, уважения к своему народу, чувства ответственности перед Родиной.',
            'icon': 'icon-flag',
            'activities': [
                'Встречи с ветеранами',
                'Военно-патриотические игры',
                'Акция "Бессмертный полк"'
            ]
        },
        {
            'title': 'Духовно-нравственное воспитание',
            'description': 'Развитие нравственных чувств и этического сознания, формирование ценностных ориентаций и моральных норм.',
            'icon': 'icon-heart',
            'activities': [
                'Тематические классные часы',
                'Благотворительные акции',
                'Волонтерская деятельность',
                'Творческие конкурсы'
            ]
        },
        {
            'title': 'Интеллектуальное воспитание',
            'description': 'Формирование ценности знания, стремления к интеллектуальному развитию и совершенствованию.',
            'icon': 'icon-book-open',
            'activities': [
                'Предметные олимпиады',
                'Интеллектуальные игры и конкурсы',
                'Проектная деятельность',

            ]
        },
        {
            'title': 'Здоровьесберегающее воспитание',
            'description': 'Формирование ценностного отношения к здоровью и здоровому образу жизни.',
            'icon': 'icon-activity',
            'activities': [
                'Спортивные соревнования',
                'Дни здоровья',
                'Профилактические беседы',
                'Туристические походы',
                'Акции против вредных привычек'
            ]
        },
        {
            'title': 'Социокультурное и медиакультурное воспитание',
            'description': 'Формирование представлений о таких понятиях, как "толерантность", "миролюбие", "социальное партнерство".',
            'icon': 'icon-users',
            'activities': [
                'Фестивали национальных культур',
                'Социальные проекты',
                'Медиапроекты',
            ]
        },
        {
            'title': 'Культуротворческое и эстетическое воспитание',
            'description': 'Формирование ценностного отношения к прекрасному, представлений об эстетических идеалах и ценностях.',
            'icon': 'icon-music',
            'activities': [
                'Посещение театров и музеев',
                'Творческие конкурсы и выставки',
                'Концерты и фестивали',
                'Художественные мастер-классы'
            ]
        },
        {
            'title': 'Правовое воспитание и культура безопасности',
            'description': 'Формирование правовой культуры, представлений об основных правах и обязанностях, о принципах демократии, об уважении к правам человека и свободе личности.',
            'icon': 'icon-shield',
            'activities': [
                'Правовые уроки',
                'Деловые игры',
                'Конкурсы правовых знаний',
            ]
        },
        {
            'title': 'Экологическое воспитание',
            'description': 'Формирование ценностного отношения к природе, окружающей среде, бережного отношения к процессу освоения природных ресурсов.',
            'icon': 'icon-leaf',
            'activities': [
                'Экологические акции',
                'Субботники',
                'Экскурсии на природу',
                'Проектная деятельность',
                'Конкурсы экологических плакатов'
            ]
        }
    ]

    # Календарь воспитательных мероприятий
    calendar = [
        {
            'month': 'Сентябрь',
            'events': [
                {'date': '1', 'title': 'День знаний',
                 'description': 'Торжественная линейка, посвященная началу учебного года.'},
                {'date': '3', 'title': 'День солидарности в борьбе с терроризмом',
                 'description': 'Классные часы, посвященные памяти жертв терроризма.'},
                {'date': '8', 'title': 'Международный день распространения грамотности',
                 'description': 'Конкурс грамотности среди учащихся.'},
                {'date': '27', 'title': 'День работника дошкольного образования',
                 'description': 'Поздравление воспитателей детского сада.'},
            ]
        },
        {
            'month': 'Октябрь',
            'events': [
                {'date': '5', 'title': 'День учителя', 'description': 'Праздничный концерт, день самоуправления.'},
                {'date': '16', 'title': 'День отца', 'description': 'Спортивные соревнования "Папа может".'},
                {'date': '25', 'title': 'Международный день школьных библиотек',
                 'description': 'Литературная гостиная, выставка книг.'},
                {'date': '28-30', 'title': 'Осенний бал', 'description': 'Праздничное мероприятие для учащихся.'},
            ]
        },
        {
            'month': 'Ноябрь',
            'events': [
                {'date': '4', 'title': 'День народного единства',
                 'description': 'Классные часы, посвященные истории праздника.'},
                {'date': '16', 'title': 'Международный день толерантности',
                 'description': 'Фестиваль национальных культур.'},
                {'date': '27', 'title': 'День матери',
                 'description': 'Праздничный концерт, конкурс рисунков "Моя мама".'},
            ]
        },
        {
            'month': 'Декабрь',
            'events': [
                {'date': '3', 'title': 'День неизвестного солдата',
                 'description': 'Уроки мужества, возложение цветов к памятнику.'},
                {'date': '9', 'title': 'День Героев Отечества',
                 'description': 'Встречи с ветеранами, конкурс сочинений.'},
                {'date': '12', 'title': 'День Конституции РФ',
                 'description': 'Правовые уроки, викторина "Знаешь ли ты Конституцию?".'},
                {'date': '25-29', 'title': 'Новогодние праздники',
                 'description': 'Утренники, вечера, конкурс на лучшее украшение класса.'},
            ]
        },
        {
            'month': 'Январь',
            'events': [
                {'date': '25', 'title': 'День российского студенчества',
                 'description': 'Встречи с выпускниками школы, студентами вузов.'},
                {'date': '27', 'title': 'День полного освобождения Ленинграда от фашистской блокады',
                 'description': 'Уроки памяти, просмотр документальных фильмов.'},
            ]
        },
        {
            'month': 'Февраль',
            'events': [
                {'date': '8', 'title': 'День российской науки',
                 'description': 'Научно-практическая конференция учащихся.'},
                {'date': '15', 'title': 'День памяти о россиянах, исполнявших служебный долг за пределами Отечества',
                 'description': 'Встречи с участниками боевых действий.'},
                {'date': '21', 'title': 'Международный день родного языка',
                 'description': 'Конкурс чтецов, литературная викторина.'},
                {'date': '23', 'title': 'День защитника Отечества',
                 'description': 'Военно-спортивная игра "Зарница", конкурс "А ну-ка, парни!".'},
            ]
        },
        {
            'month': 'Март',
            'events': [
                {'date': '8', 'title': 'Международный женский день',
                 'description': 'Праздничный концерт, конкурс "А ну-ка, девушки!".'},
                {'date': '18', 'title': 'День воссоединения Крыма с Россией',
                 'description': 'Тематические классные часы, викторина.'},
                {'date': '25-31', 'title': 'Неделя детской и юношеской книги',
                 'description': 'Литературные конкурсы, выставки, встречи с писателями.'},
            ]
        },
        {
            'month': 'Апрель',
            'events': [
                {'date': '12', 'title': 'День космонавтики',
                 'description': 'Гагаринский урок "Космос - это мы", конкурс рисунков.'},
                {'date': '21', 'title': 'День местного самоуправления',
                 'description': 'Встречи с представителями местной администрации.'},
                {'date': '30', 'title': 'День пожарной охраны',
                 'description': 'Тематический урок ОБЖ, учебная эвакуация.'},
            ]
        },
        {
            'month': 'Май',
            'events': [
                {'date': '9', 'title': 'День Победы',
                 'description': 'Участие в акции "Бессмертный полк", концерт для ветеранов.'},
                {'date': '15', 'title': 'Международный день семьи',
                 'description': 'Семейные спортивные соревнования "Мама, папа, я - спортивная семья".'},
                {'date': '24', 'title': 'День славянской письменности и культуры',
                 'description': 'Тематические уроки, выставка книг.'},
                {'date': '25', 'title': 'Последний звонок', 'description': 'Торжественная линейка для выпускников.'},
            ]
        }
    ]

    # Школьное самоуправление
    student_council = {
        'description': 'Школьное самоуправление - это форма организации жизнедеятельности коллектива учащихся, обеспечивающая развитие их самостоятельности в принятии и реализации решений для достижения общественно значимых целей.',
        'structure': [
            {
                'title': 'Президент школы',
                'name': 'Иванов Иван, 11А класс',
                'responsibilities': 'Координация работы всех органов школьного самоуправления, представление интересов учащихся в администрации школы.'
            },
            {
                'title': 'Совет старшеклассников',
                'members': '15 учащихся 9-11 классов',
                'responsibilities': 'Планирование и организация общешкольных мероприятий, решение текущих вопросов школьной жизни.'
            },
            {
                'title': 'Комитет образования',
                'members': '5 учащихся 8-11 классов',
                'responsibilities': 'Организация интеллектуальных мероприятий, помощь отстающим ученикам, проведение предметных недель.'
            },
            {
                'title': 'Комитет культуры и досуга',
                'members': '7 учащихся 8-11 классов',
                'responsibilities': 'Организация и проведение творческих мероприятий, концертов, конкурсов, дискотек.'
            },
            {
                'title': 'Комитет спорта и здоровья',
                'members': '5 учащихся 8-11 классов',
                'responsibilities': 'Организация спортивных соревнований, пропаганда здорового образа жизни.'
            },
            {
                'title': 'Комитет труда и порядка',
                'members': '6 учащихся 8-11 классов',
                'responsibilities': 'Организация дежурства по школе, субботников, трудовых акций.'
            },
            {
                'title': 'Пресс-центр',
                'members': '8 учащихся 7-11 классов',
                'responsibilities': 'Выпуск школьной газеты, освещение школьных событий, ведение социальных сетей школы.'
            }
        ],
        'achievements': [
            'Победа в районном конкурсе "Лучшее школьное самоуправление" 2022 года',
            'Организация благотворительной акции "Помоги ближнему" (собрано более 50 000 рублей для детей с ограниченными возможностями)',
            'Проведение экологической акции "Чистый поселок" (высажено 100 деревьев)',
            'Организация и проведение фестиваля "Дружба народов" с участием 5 школ района'
        ]
    }

    # Достижения учащихся
    achievements = [
        {
            'category': 'Учебные достижения',
            'items': [
                'Победители и призеры регионального этапа Всероссийской олимпиады школьников по математике, физике, химии, биологии, истории, литературе',
                'Победители Всероссийского конкурса научно-исследовательских работ "Шаг в будущее"',
                'Призеры Международной олимпиады по русскому языку',
                'Лауреаты Всероссийского конкурса "Юный исследователь"'
            ]
        },
        {
            'category': 'Спортивные достижения',
            'items': [
                'Чемпионы района по волейболу среди школьных команд',
                'Призеры областных соревнований по легкой атлетике',
                'Победители районной спартакиады школьников',
                'Призеры областных соревнований по шахматам'
            ]
        },
        {
            'category': 'Творческие достижения',
            'items': [
                'Лауреаты Всероссийского конкурса "Живая классика"',
                'Победители областного фестиваля детского творчества',
                'Призеры Международного конкурса детского рисунка',
                'Лауреаты районного конкурса хоровых коллективов'
            ]
        },
        {
            'category': 'Социальные проекты',
            'items': [
                'Победители Всероссийского конкурса социальных проектов "Я - гражданин России"',
                'Лауреаты областного конкурса "Доброволец года"',
                'Победители районного конкурса экологических проектов',
                'Призеры Всероссийской акции "Я - доброволец"'
            ]
        }
    ]

    # Полезные ресурсы
    resources = [
        {
            'title': 'Для учащихся',
            'items': [
                {'name': 'Российское движение школьников', 'url': 'https://рдш.рф/'},
                {'name': 'Всероссийский конкурс "Большая перемена"', 'url': 'https://bolshayaperemena.online/'},
                {'name': 'Портал "ПроеКТОриЯ"', 'url': 'https://proektoria.online/'},
                {'name': 'Образовательный центр "Сириус"', 'url': 'https://sochisirius.ru/'},
                {'name': 'Всероссийский конкурс "Добро не уходит на каникулы"', 'url': '#'}
            ]
        },
        {
            'title': 'Для родителей',
            'items': [
                {'name': 'Национальная родительская ассоциация', 'url': 'https://nra-russia.ru/'},
                {'name': 'Портал "Я - родитель"', 'url': 'https://www.ya-roditel.ru/'},
                {'name': 'Федеральный портал "Растим детей"', 'url': 'https://растимдетей.рф/'},
                {'name': 'Портал "Семья и дети"', 'url': '#'},
                {'name': 'Центр защиты прав и интересов детей', 'url': 'https://fcprc.ru/'}
            ]
        },
        {
            'title': 'Для педагогов',
            'items': [
                {'name': 'Единый урок', 'url': 'https://единыйурок.рф/'},
                {'name': 'Российское образование', 'url': 'https://edu.ru/'},
                {'name': 'Инфоурок', 'url': 'https://infourok.ru/'},
                {'name': 'Учительский портал', 'url': 'https://www.uchportal.ru/'},
                {'name': 'Педсовет', 'url': 'https://pedsovet.org/'}
            ]
        }
    ]

    # Контактная информация
    contact_info = {
        'name': 'Сидоров Петр Алексеевич',
        'position': 'Заместитель директора по воспитательной работе',
        'phone': '8 30 (244) 31-5-13',
        'email': 'vr@razmahnino-sosh.ru',
        'reception_hours': 'Понедельник, пятница: 14:00 - 16:00'
    }

    context = {
        'directions': directions,
        'calendar': calendar,
        'student_council': student_council,
        'achievements': achievements,
        'resources': resources,
        'contact_info': contact_info
    }

    return render(request, 'educational_work.html', context)





def food_monitoring(request):
    # Получаем активную неделю меню или первую неделю, если активной нет
    active_week = MenuWeek.objects.filter(is_active=True).first() or MenuWeek.objects.first()

    # Получаем вторую неделю (если есть)
    second_week = MenuWeek.objects.exclude(id=active_week.id).first() if active_week else None

    # Получаем расписание питания
    food_schedule = FoodSchedule.objects.all().order_by('start_time')

    # Получаем отчеты о мониторинге (последние 5), если они есть
    monitoring_reports = FoodMonitoringReport.objects.all().order_by('-date')[:5]

    # Если отчетов нет, используем заглушку
    if not monitoring_reports:
        monitoring_reports = [{
            'date': 'Нет данных',
            'event': 'Нет доступных отчетов',
            'participants': '-',
            'results': 'Нет данных',
            'report': '-'
        }]

    # Получаем документы
    food_documents = FoodDocument.objects.all().order_by('-upload_date')

    # Собираем данные о меню для каждой недели
    week_data = {}
    if active_week:
        week_data['week1'] = {
            'name': active_week.name,
            'start_date': active_week.start_date,
            'end_date': active_week.end_date,
            'days': []
        }

        # Для каждого дня недели получаем меню и блюда
        for day in active_week.days.all():
            day_data = {
                'day': day.get_day_display(),
                'menu_type': day.menu_type.name,
                'items': []
            }

            # Собираем блюда для дня
            for item in day.items.all():
                day_data['items'].append({
                    'name': item.name,
                    'description': item.description,
                    'calories': item.calories,
                    'proteins': item.proteins,
                    'fats': item.fats,
                    'carbs': item.carbohydrates,
                    'image': item.image.url if item.image else None,
                })

            week_data['week1']['days'].append(day_data)

        # Аналогично для второй недели
        if second_week:
            week_data['week2'] = {
                'name': second_week.name,
                'start_date': second_week.start_date,
                'end_date': second_week.end_date,
                'days': []
            }

            for day in second_week.days.all():
                day_data = {
                    'day': day.get_day_display(),
                    'menu_type': day.menu_type.name,
                    'items': []
                }

                # Собираем блюда для дня
                for item in day.items.all():
                    day_data['items'].append({
                        'name': item.name,
                        'description': item.description,
                        'calories': item.calories,
                        'proteins': item.proteins,
                        'fats': item.fats,
                        'carbs': item.carbohydrates,
                        'image': item.image.url if item.image else None,
                    })

                week_data['week2']['days'].append(day_data)

    # Передаем данные в шаблон
    context = {
        'primary_menu': week_data,
        'food_schedule': food_schedule,
        'monitoring_reports': monitoring_reports,
        'food_documents': food_documents,
        'page_title': 'Мониторинг питания',
        'page_description': 'Информация о школьном питании, меню, расписании и мониторинге'
    }

    return render(request, 'food_monitoring.html', context)
def quality_assessment(request):
    """
    Представление для страницы "Независимая оценка качества образования"
    """
    context = {
        'page_title': 'Независимая оценка качества образования',
        'page_description': 'Информация о независимой оценке качества образования в нашей школе'
    }
    return render(request, 'quality_assessment.html', context)

def scholarships(request):
    context = {
        'page_title': 'Стипендии и меры поддержки'
    }
    return render(request, 'scholarships.html', context)
def paid_services(request):
    context = {
        'page_title': 'Платные образовательные услуги'
    }
    return render(request, 'paid_services.html', context)

def international(request):
    context = {
        'page_title': 'Международное сотрудничество'
    }
    return render(request, 'international.html', context)

def vacant_places(request):
    context = {
        'page_title': 'Вакантные места для приема (перевода)'
    }
    return render(request, 'vacant_places.html', context)

def local_acts(request):
    context = {
        'page_title': 'Локальные акты образовательной организации'
    }
    return render(request, 'local_acts.html', context)


# @staff_member_required
# def respond_to_message(request, pk):
#     message = get_object_or_404(ContactMessage, pk=pk)
#
#     if request.method == 'POST':
#         form = ContactMessageResponseForm(request.POST, instance=message)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.response_date = timezone.now()
#             message.save()
#             messages.success(request, 'Ответ успешно сохранен.')
#             return redirect('admin:yourapp_contactmessage_changelist')
#     else:
#         form = ContactMessageResponseForm(instance=message)
#
#     return render(request, 'respond_to_message.html', {
#         'form': form,
#         'message': message,
#     })

# def respond_to_message(request, pk):
#     message = get_object_or_404(ContactMessage, pk=pk)
#     if request.method == 'POST':
#         form = ContactMessageResponseForm(request.POST, instance=message)
#         if form.is_valid():
#             message = form.save()
#             send_response_email(message)  # Отправка email
#             return redirect('success_url')
#
@staff_member_required
def respond_to_message(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)

    if request.method == 'POST':
        form = ContactMessageResponseForm(request.POST, instance=message)
        if form.is_valid():
            message = form.save(commit=False)
            message.response_date = timezone.now()
            message.save()
            messages.success(request, 'Ответ успешно сохранен.')
            return redirect('admin:yourapp_contactmessage_changelist')
    else:
        form = ContactMessageResponseForm(instance=message)

    return render(request, 'respond_to_message.html', {
        'form': form,
        'message': message,
    })
def respond_to_message(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        form = ContactMessageResponseForm(request.POST, instance=message)
        if form.is_valid():
            message = form.save()
            send_response_email(message)  # Отправка email
            return redirect('success_url')


def send_response_email(message):
    subject = f"Ответ на вашу заявку: {message.subject}"
    body = render_to_string('response_email.txt', {
        'message': message,
    })

    send_mail(
        subject,
        body,
        'noreply@yourdomain.com',
        [message.email],
        fail_silently=False,
    )
