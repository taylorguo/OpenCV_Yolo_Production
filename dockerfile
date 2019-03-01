FROM python:3
ADD . /code
WORKDIR /code
RUN pip install -r r.txt
CMD gunicorn -b 127.0.0.1:5000 wsgi:app