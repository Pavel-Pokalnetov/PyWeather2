from pprint import pprint
from jinja2 import Template
from modules.mylib import get_current_datetime
from modules.weather48 import get_weather48
from modules.weather_now import get_weather_now
from modules.weather_7day import get_weather_7day
from modules.emailer import send_html_email
import yaml


def send_weather_city(city, emails, city_name=""):
    if city_name == "":
        city_name = city
    html_template = Template(
        """<html>
            <title>Сводка погоды для {{city_name}} на {{datetime_now}}</title>
            <body>
            <h3>Сводка погоды для {{city_name}} на {{datetime_now}}</h3>
            {{weather_now}}
            {{weather48hours}}
            {{weather7day}}
            </body></html>""")

    html = html_template.render(city_name=city_name,
                                datetime_now=get_current_datetime(),
                                weather_now=get_weather_now(city,1),
                                weather48hours=get_weather48(city),
                                weather7day=get_weather_7day(city))

    send_html_email(html, emails, city_name)


if __name__ == "__main__":
    # считываем конфиг
    with open("config.yaml", "r", encoding="utf8") as f:
        data: dict = yaml.safe_load(f)

    # формируем цикл
    for config in data:
        city = config['city']
        city_name = config['cityname']
        emails = config['email']
        send_weather_city(city, emails, city_name)