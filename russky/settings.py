import logging

from pydantic import BaseSettings


class LoggingSetting(BaseSettings):
    format: str = '[%(asctime)s] <%(levelname)s> %(message)s'
    level: str = 'INFO'

    def setup(self) -> None:
        logging.basicConfig(level=self.level, format=self.format)

    class Config:
        env_prefix = 'LOGGING_'


class DataSourceSetting(BaseSettings):
    films_250_url: str = 'https://storage.yandexcloud.net/system-static.russky-devops.ru/films_top_250.json'
    shazam_top_20_url: str = 'https://storage.yandexcloud.net/system-static.russky-devops.ru/music_shazam_20.json'

    class Config:
        env_prefix = 'DATA_SOURCE_'
