FROM python:3.11-slim-buster
WORKDIR /app
COPY ./requirements.txt /app
COPY ./assets /app/assets
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=hello.py
CMD ["flask", "run", "--host", "0.0.0.0"]