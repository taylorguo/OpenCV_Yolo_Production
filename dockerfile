FROM python:3.6
RUN mkdir -p /home/code
ADD . /home/code
WORKDIR /home/code/container
RUN pip install -r r.txt -i https://pypi.douban.com/simple
EXPOSE 5000
EXPOSE 80
CMD gunicorn -b 0.0.0.0 wsgi:app