FROM python:3.10.8

WORKDIR /code

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "app:create_app()"]
