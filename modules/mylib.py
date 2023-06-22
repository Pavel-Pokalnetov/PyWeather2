import datetime
import locale
def get_digits(text):
    # фильтрует цифры из строки (оставляет только цифры)
    digits = ''
    for char in text:
        if char.isdigit():
            digits += char
    return digits

def get_current_datetime():
    # получаем время и дату в формате чч:мм ДД.ММ.ГГГГ
    # Установка локали 
    locale.setlocale(locale.LC_TIME, 'ru_RU')
    
    # Получение текущей даты и времени
    now = datetime.datetime.now()
    
    # Форматирование даты и времени
    formatted_date = now.strftime('%H:%M %d.%m.%Y г.')
    
    # Возвращение отформатированной даты и времени
    return formatted_date

if __name__=="__main__":
    print(get_current_datetime())