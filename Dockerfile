# image to up django service in docker
FROM python:3.10.11
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000
RUN python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000