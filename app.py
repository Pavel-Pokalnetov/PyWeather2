import yaml
import htmlmin
from jinja2 import Template

from modules import get_weather_now, get_weather48, get_weather_7day, send_html_email, get_current_datetime


def send_weather_city(city, emails, city_name=""):
    '''
    формирование HTML кода со сводками погоды и отправка его на почтовые адреса
    :param city:  идентификатор города
    :param emails:  список адресов
    :param city_name: название города (для обозначения в сводке)
    :return:
    '''
    if city_name == "":
        city_name = city
    html_template = Template(
        """<html>
            <title>Сводка погоды для .г{{city_name}} на {{datetime_now}}</title>
            <body>
            <h3>Сводка погоды для г.{{city_name}} на {{datetime_now}}</h3><div>
            {{weather_now}}</div>
            <h3>Почасовой прогноз погоды на 48 часов</h3><div>
            {{weather48hours}}</div>
            <h3>Сводка погоды для г.{{city_name}} на 7 дней</h3><div>
            {{weather7day}}</div>
            </body></html>""")

    html = html_template.render(city_name=city_name,
                                datetime_now=get_current_datetime(),
                                weather_now=get_weather_now(city),
                                weather48hours=get_weather48(city),
                                weather7day=get_weather_7day(city))
    html = htmlmin.minify(html)
    print(html)
    send_html_email(html, emails, city_name)


if __name__ == "__main__":
    # считываем конфиг
    with open("./config/config.yaml", "r", encoding="utf8") as f:
        data: dict = yaml.safe_load(f)

    # формируем цикл опроса и отправки
    for config in data:
        city = config['city']
        city_name = config['cityname']
        emails = config['email']
        send_weather_city(city, emails, city_name)
