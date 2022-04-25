from fastapi.testclient import TestClient

from russky.app import app
from russky.di import DI
from russky.models import MusicRecommendation

client = TestClient(app)


def test_film_recommendation():
    DI.data_sources.films.get_random_recommendation()


def test_music_recommendation():
    assert len(DI.data_sources.music.recommendations) == 20
    assert DI.data_sources.music.recommendations[0] == MusicRecommendation(
        image='https://is3-ssl.mzstatic.com/image/thumb/Music112/v4/73/b9/e4/73b9e493-5bb1-7008-8fe4-ce13b8898fe5'
        '/194690771811_cover.jpg/400x400cc.jpg',
        name='Kwaku the Traveller - Black Sherif',
        audio='https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview126/v4/62/2d/5f/622d5fdf-5fde-4c61-3440'
        '-1e7051dbc8c2/mzaf_3676952926028644501.plus.aac.ep.m4a',
    )
