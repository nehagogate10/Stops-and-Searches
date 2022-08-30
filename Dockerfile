FROM python:3.9.12-buster
COPY /flaskr/requirements.txt /flaskr/
WORKDIR /flaskr
EXPOSE 5000
RUN pip install -r requirements.txt
ENTRYPOINT [ "/bin/sh" ]
