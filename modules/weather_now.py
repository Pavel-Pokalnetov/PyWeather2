import requests
from bs4 import BeautifulSoup
from jinja2 import Template
from modules import get_current_datetime


def get_weather_now(city, debug=False):
    '''
    возвращает HTML блок таблицы для текущего прогноза
    :param city: - идентификатор города
    :param debug: - флаг для отладки(False - отладка отключена)
    :return: - блок кода HTML таблица с данными
    '''
    try:
        # URL страницы с прогнозом погоды
        url = f'https://world-weather.ru/pogoda/russia/{city}/'
        # Заголовки для запроса
        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)'
        }

        # Отправляем GET-запрос на страницу
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Ошибка загрузки данных: код ответа {response.status_code}")

        # Сохраняем страницу (для отладки)
        if debug:
            with open('./temp/weather_now.html', 'w', encoding='utf8') as htmlfile:
                htmlfile.write(response.text)
        # Создаем объект BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # актуальность данных
        update = soup.select('div.forecast-updated')[0].get_text()

        w_array = []

        # температура
        temperature = soup.select('div#weather-now-number')[0].get_text()
        w_array.append(['Температура', temperature])

        # блок погоды
        weather_block = soup.select('div#weather-now-description>dl')[0]
        w_block_size = len(weather_block.select('dt'))  #размер блока погоды (строки данных)

        for i in range(w_block_size):
            head = weather_block.select('dt')[i].text
            if head == 'Ветер':
                value = weather_block.select('dd')[i].select('span')[1].get('title') + " " + \
                        weather_block.select('dd')[i].text
            else:
                value = weather_block.select('dd')[i].text
            w_array.append([head, value])

        html = ""

        # шаблон HTML
        table_template = Template('''
        <table>{% for tr in w_array %}
        <tr>
            {% for td in tr %}
            <td>{{ td }}</td>{% endfor %}
        </tr>{% endfor %}
        </table>
        <span style="font-size: small;"><u><i>{{update}}</i></u></span>
        ''')

        # формируем блок HTML по шаблону
        html = table_template.render(timedate=get_current_datetime(),
                                     w_array=w_array,
                                     update=update)

        if debug:
            with open('./temp/w_Now.html', 'w', encoding='utf8') as htmlfile:
                htmlfile.write(html)

        return html
    except Exception as e:
        return f'<p>Возникла ошибка во время получения текущей погоды: {str(e)}</p>'


if __name__ == "__main__":
    print(get_weather_now('kurgan',True))
