import logging
import os
from dotenv import load_dotenv
from src.extractor.lastfm_client import extract_all
from src.extractor.musicbrainz_client import fetch_artist_metadata
from src.transformer.normalizer import normalize
from src.loader.supabase_loader import load
import time

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def enrich_with_musicbrainz(artists: list[dict]) -> list[dict]:
    """Enriquece cada artista com metadados da MusicBrainz."""
    enriched = []
    for i, artist in enumerate(artists):
        meta = fetch_artist_metadata(artist["name"])
        artist["_country"] = meta.get("country")
        artist["_life_span"] = meta.get("life-span", {})
        enriched.append(artist)

        if (i + 1) % 10 == 0:
            logger.info(f"MusicBrainz: {i + 1}/{len(artists)} artistas enriquecidos")

        time.sleep(1)  # rate limit MusicBrainz

    return enriched


def run():
    limit = int(os.getenv("EXTRACT_LIMIT", 50))
    min_listeners = int(os.getenv("MIN_LISTENERS", 100000))

    logger.info("=== Iniciando pipeline ===")

    logger.info("Etapa 1: Extração Last.fm")
    raw = extract_all(limit_per_genre=limit, min_listeners=min_listeners)

    logger.info("Etapa 2: Enriquecimento MusicBrainz")
    enriched = enrich_with_musicbrainz(raw)

    logger.info("Etapa 3: Transformação")
    df = normalize(enriched)
    logger.info(f"Artistas após normalização: {len(df)}")

    logger.info("Etapa 4: Carga")
    stats = load(df)

    logger.info(f"=== Pipeline concluído — {stats['loaded']} artistas carregados ===")


if __name__ == "__main__":
    run()