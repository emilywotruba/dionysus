FROM python:3.11-slim-buster
WORKDIR /app
COPY ./requirements.txt /app
COPY ./src/static /app/static
COPY ./src/templates /app/templates
COPY ./src/__main__.py /app/__main__.py
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "/app/__main__.py"]