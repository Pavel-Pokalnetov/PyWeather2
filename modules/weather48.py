import requests
from bs4 import BeautifulSoup
from jinja2 import Template

def get_weather48(city, debug=False):
    # URL страницы с прогнозом погоды
    url = f'https://world-weather.ru/pogoda/russia/{city}/24hours/'
    # Заголовки для запроса
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)'
    }
    # Отправляем GET-запрос на страницу
    response = requests.get(url, headers=headers)
    # Сохраняем страницу (для отладки)
    if debug:
        with open('./temp/weather_48.html', 'w', encoding='utf8') as htmlfile:
            htmlfile.write(response.text)
    # Создаем объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    # находим 3 даты
    days = [d.select_one('span').text + ' ' + d.text.replace(d.select_one('span').text + ', ', '') for d in
            soup.select('div.dates')]
    # Находим нужные строки таблиц
    tabbleraw = soup.find_all('table', {'class': 'weather-today'})
    htmldate = []
    for i in (1, 2, 3):
        # Находим все строки таблицы
        rows = tabbleraw[i].find_all('tr')
        tabble = []
        # Проходимся по каждой строке и извлекаем информацию
        for row in rows:
            # Ищем тег <td> с классом "weather-day" и получаем время
            time = row.find('td', {'class': 'weather-day'}).text

            # Ищем тег <td> с классом "weather-temperature" и получаем температуру
            temperature = row.find('td', {'class': 'weather-temperature'}).find('span').text
            cloudiness = row.find('td', {'class': 'weather-temperature'}).find('div').get('title')
            # Ищем тег <td> с классом "weather-feeling" и получаем ощущаемую температуру
            feeling_temperature = row.find('td', {'class': 'weather-feeling'}).text

            # Ищем тег <td> с классом "weather-probability" и получаем вероятность осадков
            precipitation_probability = row.find('td', {'class': 'weather-probability'}).text

            # Ищем тег <td> с классом "weather-pressure" и получаем давление
            pressure = row.find('td', {'class': 'weather-pressure'}).text + " мм/р.ст."

            # Ищем тег <td> с классом "weather-wind" и получаем скорость ветра
            wind = row.find('td', {'class': 'weather-wind'}).find_all('span')
            wind_direction = wind[0].get('title') + " "
            wind_speed = wind[1].text.strip() + "м/с"

            tabble.append(
                [time, cloudiness, temperature + "/<i>" + feeling_temperature + "</i>", precipitation_probability,
                 pressure,
                 wind_direction + wind_speed])
        htmldate.append(tabble)
    # заготовка для HTML блока
    html = """<div>
<h3>Почасовой прогноз погоды на 48 часов</h3>
"""
    # шаблон HTML
    table_template = Template('''
    <b>{{days}}</b>
    <table  border="1" style="border-collapse:collapse;">
        <thead style="font-size: medium;padding: 10px;">
            <tr>
                <th style="padding: 10px;">Время</th>
                <th style="padding: 10px;">Атмосферные явления</th>
                <th style="padding: 10px;">Температура/<br><i>Ощущаемая температура</i></th>
                <th style="padding: 10px;">Вероятность осадков</th>
                <th style="padding: 10px;">Атмосферное давление</th>
                <th style="padding: 10px;">Ветер</th>
            </tr>
        </thead>
        <tbody style="font-size: smaller;padding: 10px;">
        {% for row in data %}
            <tr>
            {% for cell in row %}
                <td><center>{{ cell }}</center></td>
            {% endfor %}
            </tr>
        {% endfor %}
        </tbody>
    </table>
''')
    # собираем html по шаблону
    for i in (0, 1, 2):
        html += table_template.render(data=htmldate[i], days=days[i])
    html+="</div>"
    # сформированный блок (для отладки)
    if debug:
        with open('./temp/w_48.html', 'w', encoding='utf8') as htmlfile:
            htmlfile.write(html)

    return  html

