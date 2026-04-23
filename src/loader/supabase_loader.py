import logging
import os
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def get_client() -> Client:
    """Cria e retorna o cliente Supabase."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("SUPABASE_URL e SUPABASE_KEY precisam estar no .env")

    return create_client(url, key)


def load(df: pd.DataFrame) -> dict:
    """Faz upsert dos artistas no Supabase e retorna estatísticas."""
    client = get_client()

    # Remove duplicatas — mantém o primeiro gênero encontrado
    df = df.drop_duplicates(subset="artist_id", keep="first")

    records = df.where(pd.notna(df), None).to_dict(orient="records")

    records = [
        {k: (None if isinstance(v, float) and v != v else v) for k, v in r.items()}
        for r in records
    ]

    client.table("artists").upsert(records, on_conflict="artist_id").execute()

    stats = {"loaded": len(records)}
    logger.info(f"Carregados {stats['loaded']} artistas no Supabase")

    return stats