<p align="center" width="100%">
    <img width="33%" src="./src/static/logo.png">
</p>

# Dionysus

Self-hosted web interface that allows users to search for movies and shows across multiple streaming services in multiple countries, grouped by streaming service.

## Use
#### Bash:
```bash
git clone https://github.com/emilywotruba/dionysus.git
cd dionysus
python3.11 -m pip install -r requirements.txt
cd src
python3.11 .
```
#### Docker:
```bash
docker run -p 5000:5000 ghcr.io/emilywotruba/dionysus:latest
```
#### Docker-Compose:
```bash
git clone https://github.com/emilywotruba/dionysus.git
cd dionysus
docker-compose up -d
```

## Build
```bash
git clone https://github.com/emilywotruba/dionysus.git
cd dionysus
sudo docker build -t dionysus .
```
