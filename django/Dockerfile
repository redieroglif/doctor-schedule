FROM python:3.6

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN apt-get update && apt-get install -y --no-install-recommends supervisor
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY ./src /app/src
COPY ./supervisor-app.conf /etc/supervisor/conf.d/

CMD python /app/src/manage.py migrate && python /app/src/manage.py collectstatic -v0 --noinput && supervisord -n
