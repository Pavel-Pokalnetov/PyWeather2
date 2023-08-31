import yaml
import htmlmin
from jinja2 import Template
from modules import get_current_datetime
from modules import get_weather48
from modules import get_weather_now
from modules import get_weather_7day
from modules import send_html_email


def send_weather_city(city, emails, city_name=""):
    if city_name == "":
        city_name = city
    html_template = Template(
        """<html>
            <title>Сводка погоды для .г{{city_name}} на {{datetime_now}}</title>
            <body>
            <h3>Сводка погоды для г.{{city_name}} на {{datetime_now}}</h3>
            {{weather_now}}
            {{weather48hours}}
            <h3>Сводка погоды для г.{{city_name}} на 7 дней</h3>
            {{weather7day}}
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
    with open("config.yaml", "r", encoding="utf8") as f:
        data: dict = yaml.safe_load(f)

    # формируем цикл опроса и отправки
    for config in data:
        city = config['city']
        city_name = config['cityname']
        emails = config['email']
        send_weather_city(city, emails, city_name)
