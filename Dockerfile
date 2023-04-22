FROM python:3

ENV PYTHONBUFFERED=1

WORKDIR /DRF

COPY ./DRF/requirements.txt .
COPY ./DRF/ .

RUN python -m pip install -r ./requirements.txt



CMD ["python","manage.py","runserver" ,"0.0.0.0:8000"]




