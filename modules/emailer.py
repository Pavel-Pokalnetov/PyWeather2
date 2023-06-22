import yaml
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_html_email(html, to_emails, city_name):
    """
    Отправляет HTML-письмо на список почтовых адресов.

    :param html: HTML-код письма.
    :param to_emails: Список почтовых адресов получателей.
    :param citi_name: Реальное название города
    """
    # 
    with open('./modules/emailcfg.yaml', 'r') as cfg_file:
        config = yaml.safe_load(cfg_file)

    smtp_server = config['smtp_server']
    smtp_port = config['smtp_port']
    smtp_username = config['smtp_username']
    smtp_password = config['smtp_password']

    msg = MIMEMultipart()

    # заголовок и текст письма
    msg['From'] = config['smtp_username']
    msg['Subject'] = f"Сводка погоды г.{city_name}"
    msg.attach(MIMEText(html, 'html'))
    
    # Отправляем письмо на каждый адрес в списке
    for to_email in to_emails:
        try:
            # Создаем SMTP объект и подключаемся к почтовому серверу
            smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
            smtp_connection.starttls()
            smtp_connection.login(smtp_username, smtp_password)

            # Отправляем письмо
            msg['To'] = to_email
            smtp_connection.sendmail(smtp_username, to_email, msg.as_string())

            # Закрываем соединение
            smtp_connection.quit()

            print(f'Письмо со сводкой для г.{city_name} успешно отправлено на адрес {to_email}')
        except Exception as e:
            print(f'Ошибка отправки письма со сводкой для г.{city_name} на адрес {to_email}: {e}')