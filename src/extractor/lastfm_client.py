import os
import time
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

BASE_URL = "http://ws.audioscrobbler.com/2.0/"
API_KEY = os.getenv("LASTFM_KEY")

GENRES = [
    "rock", "pop", "jazz", "metal", "hip-hop",
    "electronic", "classical", "blues", "reggae", "punk",
    "country", "r&b", "soul", "folk", "latin",
    "alternative", "indie", "funk", "gospel", "disco"
]


def fetch_top_artists_by_genre(genre: str, limit: int = 200) -> list[dict]:
    """Busca os top artistas de um gênero na Last.fm."""
    artists = []
    page = 1
    per_page = 50  # Last.fm retorna no máximo 50 por página

    while len(artists) < limit:
        params = {
            "method": "tag.gettopartists",
            "tag": genre,
            "api_key": API_KEY,
            "format": "json",
            "limit": per_page,
            "page": page
        }

        try:
            response = requests.get(BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            page_artists = data.get("topartists", {}).get("artist", [])
            if not page_artists:
                break

            artists.extend(page_artists)
            logger.info(f"Last.fm '{genre}' página {page}: {len(page_artists)} artistas")
            page += 1
            time.sleep(0.25)

        except Exception as e:
            logger.warning(f"Last.fm erro para '{genre}' página {page}: {e}")
            break

    return artists[:limit]


def fetch_artist_info(artist_name: str) -> dict:
    """Busca listeners e info de um artista na Last.fm."""
    params = {
        "method": "artist.getinfo",
        "artist": artist_name,
        "api_key": API_KEY,
        "format": "json"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("artist", {})
    except Exception as e:
        logger.warning(f"Last.fm getinfo erro para '{artist_name}': {e}")
        return {}


def extract_all(limit_per_genre: int = 200, min_listeners: int = 20000) -> list[dict]:
    """Extrai top artistas de todos os gêneros."""
    all_artists = []

    for genre in GENRES:
        logger.info(f"Extraindo gênero: {genre}")
        top_artists = fetch_top_artists_by_genre(genre, limit=limit_per_genre)

        for artist in top_artists:
            # Busca listeners individualmente
            info = fetch_artist_info(artist["name"])
            listeners = int(info.get("stats", {}).get("listeners", 0))

            if listeners >= min_listeners:
                artist["_genre"] = genre
                artist["listeners"] = listeners
                all_artists.append(artist)

            time.sleep(0.25)

        count = len([a for a in all_artists if a.get("_genre") == genre])
        logger.info(f"Gênero '{genre}': {count} artistas com {min_listeners}+ listeners")

    logger.info(f"Total extraído: {len(all_artists)} artistas")
    return all_artists