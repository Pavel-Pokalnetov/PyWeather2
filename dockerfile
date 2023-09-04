FROM python:3

WORKDIR /usr/src/app

RUN mkdir ./modules
RUN mkdir ./config

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "/usr/src/app/app.py" ]