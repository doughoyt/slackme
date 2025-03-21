FROM python:3.10-alpine

EXPOSE 5000

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app.py app.py

CMD [ "python3", "-u", "-m" , "flask", "run", "--host=0.0.0.0"]