from pydantic import BaseSettings


class DataSourceSetting(BaseSettings):
    films_250_url: str = 'https://storage.yandexcloud.net/system-static.russky-devops.ru/films_top_250.json'
    shazam_top_20_url: str = 'https://storage.yandexcloud.net/system-static.russky-devops.ru/music_shazam_20.json'

    class Config:
        env_prefix = 'DATA_SOURCE_'
