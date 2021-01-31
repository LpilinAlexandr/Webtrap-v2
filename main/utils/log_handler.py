

def format_message(message_dict: dict):
    """
    Преобразует словарь для логирования в строку
    :param message_dict: Словарь с параметрами для логирования
    :return: Готовую строку для логирования
    """
    text = ''
    for key, value in message_dict.items():
        text += f" {key}: {value};"

    return text
