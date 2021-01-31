from django.shortcuts import render, resolve_url
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound
from django.utils import timezone
from .utils.log_handler import format_message
import logging


api_logger = logging.getLogger('api')
email_logger = logging.getLogger('email')


def email_view(request):
    """
    Страница для ввода е-меила
    """

    if request.method == 'POST':
        email = request.POST.get('email')
        # создаём словарь для логирования
        message_dict = {
            'time': timezone.now(),
            'url': request.META['HTTP_REFERER'],
            'method': request.method,
            'params': email,
        }
        # логируем
        email_logger.info(format_message(message_dict))

    return render(request, 'main/email.html', )


@csrf_exempt
def api_view(request):
    """
    Страница для API запросов
    """
    # Словарь для логирования определяем заранее, чтобы не дублировать
    message_dict = {
        'time': timezone.now(),
        'url': resolve_url('api'),
        'params': f'{[f"{key}: {value}" for key, value in request.GET.items()]}',
        'method': request.method
    }

    # Проверяем параметр method. Он должен быть равен "ping"
    method = request.GET.get('method') == 'ping'
    if request.method == 'POST' and method:
        message_dict['status'] = 200
        api_logger.info(format_message(message_dict))
        # Возвращаем 200
        return HttpResponse('ok')
    # Если параметры проверку не прошли
    elif request.method == 'POST':
        response = HttpResponse('no')
        # Возвращаем 400
        response.status_code = 400
        message_dict['status'] = response.status_code
        api_logger.info(format_message(message_dict))
        return response
    # Если это GET
    else:
        message_dict['status'] = 404
        api_logger.info(format_message(message_dict))
        # Возвращаем 404
        return HttpResponseNotFound(':(')

