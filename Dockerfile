FROM python:3

ENV PYTHONBUFFERED=1

WORKDIR /code

COPY ./DRF/requirements.txt .

COPY ./DRF/ .

RUN python -m pip install -r ./requirements.txt

EXPOSE 8000

RUN python manage.py makemigrations 

RUN python manage.py makemigrations phonebook

RUN python manage.py migrate

RUN python manage.py collectstatic 

RUN coverage run --source='.' manage.py test 

RUN coverage html

VOLUME [ "/data" ]

CMD ["python","manage.py","runserver" ,"0.0.0.0:8000"]




