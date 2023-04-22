FROM python:3

ENV PYTHONBUFFERED=1

WORKDIR /code

COPY ./DRF/ .

RUN python -m pip install -r ./requirements.txt &&\
    python manage.py makemigrations &&\
    python manage.py makemigrations phonebook &&\
    python manage.py migrate &&\
    coverage run --source='.' manage.py test &&\
    coverage html &&\
    mv coverage_html_report phonebook

VOLUME [ "/data" ]

EXPOSE 8000

CMD ["python","manage.py","runserver" ,"0.0.0.0:8000"]




