# AnimeWorld Downloader
### Using https://github.com/MainKronos/AnimeWorld-API

This project aim to download episodes from [AnimeWorld](https://www.animeworld.ac/) site.

One of the major feature is to decide if download the entirely file or the **.strm** one.

## Installation
### Docker Compose
```yaml
version: '3.9'
services:
  animeworld-downloader:
    container_name: animeworld-downloader
    volumes:
      - '/path/to/download:/app/download'
    ports:
      - '5000:5000'
    environment:
      - 'ANIMEWORLD_URL=https://www.animeworld.ac'
    image: 'ghcr.io/mainkronos/anime_downloader:latest'
```
### Python
1) `pip install -r requirements.txt`
2) `python app.py`
