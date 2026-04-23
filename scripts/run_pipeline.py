import logging
import os
from dotenv import load_dotenv
from src.extractor.musicbrainz_client import extract_all
from src.transformer.normalizer import normalize
from src.loader.supabase_loader import load

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def run():
    limit = int(os.getenv("EXTRACT_LIMIT", 100))

    logger.info("=== Iniciando pipeline ===")

    logger.info("Etapa 1: Extração")
    raw = extract_all(limit_per_genre=limit)

    logger.info("Etapa 2: Transformação")
    df = normalize(raw)
    logger.info(f"Artistas após normalização: {len(df)}")

    logger.info("Etapa 3: Carga")
    stats = load(df)

    logger.info(f"=== Pipeline concluído — {stats['loaded']} artistas carregados ===")


if __name__ == "__main__":
    run()