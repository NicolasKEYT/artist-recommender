import time
import logging
import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://musicbrainz.org/ws/2"
HEADERS = {
    "User-Agent": "ArtistRecommender/1.0 (github.com/NicolasKEYT/artist-recommender)"
}


def fetch_artist_metadata(artist_name: str) -> dict:
    """Busca metadados de um artista na MusicBrainz por nome."""
    params = {
        "query": f'artist:"{artist_name}"',
        "limit": 1,
        "fmt": "json"
    }

    try:
        response = requests.get(f"{BASE_URL}/artist", headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        artists = response.json().get("artists", [])
        if artists:
            return artists[0]
    except Exception as e:
        logger.warning(f"MusicBrainz erro para '{artist_name}': {e}")

    return {}