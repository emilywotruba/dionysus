<p align="center">
  <img src="https://github.com/emilywotruba/dionysus/blob/main/logo.jpeg?raw=true" alt="Dionysus Logo"/>
</p>

# Dionysus

Self-hosted web interface that allows users to search for movies and shows across multiple streaming services in multiple countries, grouped by streaming service.

## Use
#### Bash:
```bash
python3.11 hello.py
```
#### Docker:
```bash
docker run -p 5000:5000 ghcr.io/emilywotruba/dionysus:main
```
#### Docker-Compose:
```bash
docker-compose up -d
```

## Build
```bash
sudo docker build -t dionysus .
```