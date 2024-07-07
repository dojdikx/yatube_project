from django.shortcuts import render
from django.http import HttpResponse


# Главная страница
def index(request):
    return HttpResponse(
        'Ты <i>не можешь</i> получить правильные <b>ответы</b>,<br> '
        'если у тебя нет правильных <s>вопросов</s> запросов.'
    )

# Страница с груп постами;
# view-функция принимает параметр pk из path()
def group_posts(request, slug):
    return HttpResponse(f'Вы ввели: {slug}')