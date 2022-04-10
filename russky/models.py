from enum import Enum
from typing import Union

from pydantic import BaseModel


class RecommendationType(Enum):
    film = 'film'
    music = 'music'


class FilmRecommendation(BaseModel):
    type: RecommendationType = RecommendationType.film
    image: str
    name: str


class MusicRecommendation(BaseModel):
    type: RecommendationType = RecommendationType.music
    image: str
    name: str
    audio: str


class RecommendationResponse(BaseModel):
    recommendation: Union[MusicRecommendation, FilmRecommendation]
