import time
import logging
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

BASE_URL = "https://musicbrainz.org/ws/2"
HEADERS = {
    "User-Agent": "ArtistRecommender/1.0 (github.com/NicolasKEYT/artist-recommender)"
}

GENRES = [
    "rock", "pop", "jazz", "metal", "hip-hop",
    "electronic", "classical", "blues", "reggae", "punk"
]


def fetch_artists_by_genre(genre: str, limit: int = 100, offset: int = 0) -> list[dict]:
    """Busca artistas de um gênero na MusicBrainz API."""
    params = {
        "query": f'tag:"{genre}"',
        "limit": limit,
        "offset": offset,
        "fmt": "json"
    }

    response = requests.get(f"{BASE_URL}/artist", headers=HEADERS, params=params)
    response.raise_for_status()

    data = response.json()
    artists = data.get("artists", [])

    logger.info(f"Gênero '{genre}' offset {offset}: {len(artists)} artistas recebidos")
    return artists


def extract_all(limit_per_genre: int = 100) -> list[dict]:
    """Extrai artistas de todos os gêneros definidos."""
    all_artists = []

    for genre in GENRES:
        logger.info(f"Extraindo gênero: {genre}")

        artists = fetch_artists_by_genre(genre, limit=limit_per_genre)
        for artist in artists:
            artist["_genre"] = genre  # guarda o gênero que gerou esse resultado

        all_artists.extend(artists)
        time.sleep(1)  # respeita o rate limit da API (1 req/segundo)

    logger.info(f"Total extraído: {len(all_artists)} artistas")
    return all_artists