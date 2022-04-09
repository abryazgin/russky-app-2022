import logging
from typing import List

from pydantic import BaseSettings


class LoggingSetting(BaseSettings):
    format: str = '[%(asctime)s] <%(levelname)s> %(message)s'
    level: str = 'INFO'

    def setup(self) -> None:
        logging.basicConfig(level=self.level, format=self.format)

    class Config:
        env_prefix = 'LOGGING_'


class CORSSettings(BaseSettings):
    enabled: bool = True
    origins: List[str] = ['http://localhost', 'http://localhost:8000']

    class Config:
        env_prefix = 'CORS'
