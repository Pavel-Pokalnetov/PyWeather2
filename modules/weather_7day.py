from pprint import pprint
import requests
from bs4 import BeautifulSoup
from jinja2 import Template


def get_weather_stats(weather_dict: dict):
    '''
    получение и обработка статистики по температурным данным:
    расчет минимальной, максимальной и среднесуточной температуры
    :param weather_dict: словарь с погодными данными
    :return: min_temp, max_temp, avg_temp: значение минимальной максимальной и средней дневной температуры
    '''
    min_temp = max_temp = None
    avg_temp = 0
    for item in weather_dict.values():
        temp = int(item['temperature'].strip('°'))
        if min_temp == None:
            min_temp = temp
        elif min_temp > temp:
            min_temp = temp
        if max_temp == None:
            max_temp = temp
        elif max_temp < temp:
            max_temp = temp
        avg_temp += temp
    avg_temp /= 4
    return min_temp, max_temp, avg_temp


def get_weather_7day(city,debug=False):
    '''
    получение блока погоды на неделю
    :param city: - идентификатор города
    :param debug: - флаг отладки (False - отладка выкл)
    :return: - блок HTML кода со таблицей погодных данных
    '''
    try:
        # URL страницы с прогнозом погоды
        url = f'https://world-weather.ru/pogoda/russia/{city}/7days/'
        # Заголовки для запроса
        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)'
        }
        # Отправляем GET-запрос на страницу
        response = requests.get(url, headers=headers)

        if response.status_code!=200:
            raise Exception(f"Ошибка загрузки данных: код ответа {response.status_code}")

        # Сохраняем страницу (для отладки)
        if debug:
            with open('./temp/weather7day.html', 'w', encoding='utf8') as htmlfile:
                htmlfile.write(response.text)
        
        # Создаем объект BeautifulSoup для парсинга HTML
        soup_all = BeautifulSoup(response.content, 'html.parser')

        # данные для формирования таблицы
        weatherdata = {}

        # погодные блоки (7 дней)
        update = soup_all.select('div.weather-short')

        index = 0

        for weather_blok in update:
            date = weather_blok.find(
                'div', {'class': ['dates short-d', 'dates short-d red']}).text
            weather_dict = {}

            for row in weather_blok.find('table', {'class': 'weather-today short'}).find_all('tr'):
                time_of_day = row['class'][0]
                weather_dict[time_of_day] = {}
                columns = row.find_all('td')
                # время суток
                weather_dict[time_of_day]['time_of_day'] = columns[0].text
                # температура
                weather_dict[time_of_day]['temperature'] = columns[1].find(
                    'span').text
                # ощущаемая температура
                weather_dict[time_of_day]['feeling'] = columns[2].text
                # вероятность осадков
                weather_dict[time_of_day]['probability'] = columns[3].text
                # атмосферное давление
                weather_dict[time_of_day]['pressure'] = columns[4].text
                # ветер
                weather_dict[time_of_day]['wind'] = columns[5].find('span')['title'] + " " + \
                    columns[5].find_all('span')[1].text + "м/с"
                # влажность
                weather_dict[time_of_day]['humidity'] = columns[6].text

            weatherdata[index] = {}
            tmax, tmin, tavg = get_weather_stats(weather_dict)
            weatherdata[index]['date'] = date + \
                f" Температура:  минимум:{tmax}°,  максимум:{tmin}°,  среднесуточная:{round(tavg,1)}°"
            weatherdata[index]['weather'] = weather_dict
            index += 1

        html = ""
        table_template = Template("""
    {{ date }}
    <table border="1" style="border-collapse:collapse;width: 1000px;">
    <tr>
        <th style="width: 20%;"></th>
        <th style="text-align: center;width: 20%;">Ночь</th>
        <th style="text-align: center;width: 20%;">Утро</th>
        <th style="text-align: center;width: 20%;">День</th>
        <th style="text-align: center;width: 20%;">Вечер</th>
        
    </tr>
    <tr>
        <td style="text-align: center;">Температура</td>
        <td style="text-align: center;">{{ weather.night.temperature }}</td>
        <td style="text-align: center;">{{ weather.morning.temperature }}</td>
        <td style="text-align: center;">{{ weather.day.temperature }}</td>
        <td style="text-align: center;">{{ weather.evening.temperature }}</td>
        
    </tr>
    <tr>
        <td style="text-align: center;">Ощущается как</td>
        <td style="text-align: center;">{{ weather.night.feeling }}</td>
        <td style="text-align: center;">{{ weather.morning.feeling }}</td>
        <td style="text-align: center;">{{ weather.day.feeling }}</td>
        <td style="text-align: center;">{{ weather.evening.feeling }}</td>
        
    </tr>
    <tr>
        <td style="text-align: center;">Влажность</td>
        <td style="text-align: center;">{{ weather.night.humidity }}</td>
        <td style="text-align: center;">{{ weather.morning.humidity }}</td>
        <td style="text-align: center;">{{ weather.day.humidity }}</td>
        <td style="text-align: center;">{{ weather.evening.humidity }}</td>
        
    </tr>
    <tr>
        <td style="text-align: center;">Давление</td>
        <td style="text-align: center;">{{ weather.night.pressure }}</td>
        <td style="text-align: center;">{{ weather.morning.pressure }}</td>
        <td style="text-align: center;">{{ weather.day.pressure }}</td>
        <td style="text-align: center;">{{ weather.evening.pressure }}</td>
        
    </tr>
    <tr>
        <td style="text-align: center;">Вероятность осадков</td>
        <td style="text-align: center;">{{ weather.night.probability }}</td>
        <td style="text-align: center;">{{ weather.morning.probability }}</td>
        <td style="text-align: center;">{{ weather.day.probability }}</td>
        <td style="text-align: center;">{{ weather.evening.probability }}</td>
        
    </tr>
    <tr>
        <td style="text-align: center;">Ветер</td>
        <td style="text-align: center;">{{ weather.night.wind }}</td>
        <td style="text-align: center;">{{ weather.morning.wind }}</td>
        <td style="text-align: center;">{{ weather.day.wind }}</td>
        <td style="text-align: center;">{{ weather.evening.wind }}</td>
        
    </tr>
    </table><br>
    """)

        for i in (0, 1, 2, 3, 4, 5, 6):
            html += table_template.render(weatherdata[i])

        if debug:
            with open('./temp/w_7day.html', 'w', encoding='utf8') as htmlfile:
                htmlfile.write(html)

        return html
    except Exception as e:
        return f'<p>Возникла ошибка во время получения прогноза на 7 дней: {str(e)}'

if __name__ == "__main__":
    get_weather_7day(1)
