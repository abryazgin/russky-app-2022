import logging
import random
from typing import Dict, List, Union

import elasticapm
import requests

from russky.models import FilmRecommendation, MusicRecommendation, RecommendationType
from russky.settings import DataSourceSetting

logger = logging.getLogger(__name__)


class MulitpleDataSources:
    def __init__(self, data_source_settings: DataSourceSetting):
        logger.info('MulitpleDataSources: started')
        self.films = FilmsDataSource(data_source_settings.films_250_url)
        self.music = ShazamDataSource(data_source_settings.shazam_top_20_url)
        self.data_sources_map: Dict[str, Union[FilmsDataSource, ShazamDataSource]] = {
            RecommendationType.film.name: self.films,
            RecommendationType.music.name: self.music,
        }
        self.data_sources: List[Union[FilmsDataSource, ShazamDataSource]] = list(self.data_sources_map.values())
        logger.info('MulitpleDataSources: prepared')

    @elasticapm.capture_span('MulitpleDataSources.get_random_recommendation')
    def get_random_recommendation(self) -> Union[FilmRecommendation, MusicRecommendation]:
        return random.choice(self.data_sources).get_random_recommendation()

    @elasticapm.capture_span('MulitpleDataSources.get_random_recommendation_by_type')
    def get_random_recommendation_by_type(
        self, recommendation_type: str
    ) -> Union[FilmRecommendation, MusicRecommendation]:
        return self.data_sources_map[recommendation_type].get_random_recommendation()


class FilmsDataSource:
    """
    Sample:

    {
        "items": [
            {
                "id": "tt0111161",
                "rank": "1",
                "title": "The Shawshank Redemption",
                "fullTitle": "The Shawshank Redemption (1994)",
                "year": "1994",
                "image": "https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UX128_CR0,3,128,176_AL_.jpg",
                "crew": "Frank Darabont (dir.), Tim Robbins, Morgan Freeman",
                "imDbRating": "9.2",
                "imDbRatingCount": "2570848"
            },
        ]
    }
    """  # noqa

    def __init__(self, url: str):
        logger.info('FilmsDataSource: started')
        cache = requests.get(url).json()
        self.recommendations = [
            FilmRecommendation(
                image=i['image'].split(',')[0],
                name=i['fullTitle'],
            )
            for i in cache['items']
        ]
        logger.info('FilmsDataSource: prepared')

    @elasticapm.capture_span('FilmsDataSource.get_random_recommendation')
    def get_random_recommendation(self) -> FilmRecommendation:
        return random.choice(self.recommendations)


class ShazamDataSource:
    """
    Sample

    {
        "properties": {},
        "tracks": [
            {
                "layout": "5",
                "type": "MUSIC",
                "key": "605670552",
                "title": "Kwaku the Traveller",
                "subtitle": "Black Sherif",
                "share": {
                    "subject": "Kwaku the Traveller - Black Sherif",
                    "text": "I used Shazam to discover Kwaku the Traveller by Black Sherif.",
                    "href": "https://www.shazam.com/track/605670552/kwaku-the-traveller",
                    "image": "https://is3-ssl.mzstatic.com/image/thumb/Music112/v4/73/b9/e4/73b9e493-5bb1-7008-8fe4-ce13b8898fe5/194690771811_cover.jpg/400x400cc.jpg",
                    "twitter": "I used @Shazam to discover Kwaku the Traveller by Black Sherif.",
                    "html": "https://www.shazam.com/snippets/email-share/605670552?lang=en-US&country=US",
                    "avatar": "https://is5-ssl.mzstatic.com/image/thumb/Music116/v4/d3/d9/b7/d3d9b73c-52a2-a524-2ecb-2237a4bc7857/pr_source.png/800x800cc.jpg",
                    "snapchat": "https://www.shazam.com/partner/sc/track/605670552"
                },
                "images": {
                    "background": "https://is5-ssl.mzstatic.com/image/thumb/Music116/v4/d3/d9/b7/d3d9b73c-52a2-a524-2ecb-2237a4bc7857/pr_source.png/800x800cc.jpg",
                    "coverart": "https://is3-ssl.mzstatic.com/image/thumb/Music112/v4/73/b9/e4/73b9e493-5bb1-7008-8fe4-ce13b8898fe5/194690771811_cover.jpg/400x400cc.jpg",
                    "coverarthq": "https://is3-ssl.mzstatic.com/image/thumb/Music112/v4/73/b9/e4/73b9e493-5bb1-7008-8fe4-ce13b8898fe5/194690771811_cover.jpg/400x400cc.jpg",
                    "joecolor": "b:cc2d00p:f9f5fds:fdf2eft:f0cdcaq:f3cabf"
                },
                "hub": {
                    "type": "APPLEMUSIC",
                    "image": "https://images.shazam.com/static/icons/hub/web/v5/applemusic.png",
                    "actions": [
                        {
                            "name": "apple",
                            "type": "applemusicplay",
                            "id": "1611260776"
                        },
                        {
                            "name": "apple",
                            "type": "uri",
                            "uri": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview126/v4/62/2d/5f/622d5fdf-5fde-4c61-3440-1e7051dbc8c2/mzaf_3676952926028644501.plus.aac.ep.m4a"
                        }
                    ],
                    "options": [
                        {
                            "caption": "OPEN",
                            "actions": [
                                {
                                    "name": "hub:applemusic:deeplink",
                                    "type": "applemusicopen",
                                    "uri": "https://music.apple.com/us/album/kwaku-the-traveller/1611260775?i=1611260776&mttnagencyid=s2n&mttnsiteid=125115&mttn3pid=Apple-Shazam&mttnsub1=Shazam_web&mttnsub2=5348615A-616D-3235-3830-44754D6D5973&itscg=30201&app=music&itsct=Shazam_web"
                                },
                                {
                                    "name": "hub:applemusic:deeplink",
                                    "type": "uri",
                                    "uri": "https://music.apple.com/us/album/kwaku-the-traveller/1611260775?i=1611260776&mttnagencyid=s2n&mttnsiteid=125115&mttn3pid=Apple-Shazam&mttnsub1=Shazam_web&mttnsub2=5348615A-616D-3235-3830-44754D6D5973&itscg=30201&app=music&itsct=Shazam_web"
                                }
                            ],
                            "beacondata": {
                                "type": "open",
                                "providername": "applemusic"
                            },
                            "image": "https://images.shazam.com/static/icons/hub/web/v5/overflow-open-option.png",
                            "type": "open",
                            "listcaption": "Open in Apple Music",
                            "overflowimage": "https://images.shazam.com/static/icons/hub/web/v5/applemusic-overflow.png",
                            "colouroverflowimage": false,
                            "providername": "applemusic"
                        }
                    ],
                    "explicit": true,
                    "displayname": "APPLE MUSIC"
                },
                "artists": [
                    {
                        "follow": {
                            "followkey": "A_207047915"
                        },
                        "alias": "black-sherif",
                        "id": "207047915",
                        "adamid": "1485819772"
                    }
                ],
                "url": "https://www.shazam.com/track/605670552/kwaku-the-traveller",
                "highlightsurls": {
                    "artisthighlightsurl": "https://cdn.shazam.com/video/v3/en-US/US/web/1485819772/highlights?affiliate=mttnagencyid%3Ds2n%26mttnsiteid%3D125115%26mttn3pid%3DApple-Shazam%26mttnsub1%3DShazam_web%26mttnsub2%3D5348615A-616D-3235-3830-44754D6D5973%26itscg%3D30201%26app%3Dmusic%26itsct%3DShazam_web",
                    "relatedhighlightsurl": "https://cdn.shazam.com/video/v3/en-US/US/web/207047915/artist-similarities-id-207047915/relatedhighlights?max_artists=5&affiliate=mttnagencyid%3Ds2n%26mttnsiteid%3D125115%26mttn3pid%3DApple-Shazam%26mttnsub1%3DShazam_web%26mttnsub2%3D5348615A-616D-3235-3830-44754D6D5973%26itscg%3D30201%26app%3Dmusic%26itsct%3DShazam_web"
                },
                "properties": {}
            },
        ]
    }
    """  # noqa

    def __init__(self, url: str):
        logger.info('ShazamDataSource: started')
        cache = requests.get(url).json()
        self.recommendations = [
            MusicRecommendation(
                image=i['images']['coverart'],
                name=i['share']['subject'],
                audio=i['hub']['actions'][1]['uri'],
            )
            for i in cache['tracks']
        ]
        logger.info('ShazamDataSource: prepared')

    @elasticapm.capture_span('ShazamDataSource.get_random_recommendation')
    def get_random_recommendation(self) -> MusicRecommendation:
        return random.choice(self.recommendations)
