import pandas as pd
import logging

logger = logging.getLogger(__name__)


def normalize(artists_raw: list[dict]) -> pd.DataFrame:
    """Transforma a lista bruta da API num DataFrame limpo."""
    df = pd.DataFrame(artists_raw)

    df["artist_id"] = df["id"]
    df["name"] = df["name"].str.strip()
    df["genre"] = df["_genre"]
    df["country"] = df.get("country", pd.Series(dtype="str"))
    df["begin_year"] = df["life-span"].apply(_extract_year)
    df["decade_start"] = df["begin_year"].apply(_to_decade)

    # Converte para Int64 (aceita None, diferente do int normal)
    df["begin_year"] = pd.array(df["begin_year"], dtype="Int64")
    df["decade_start"] = pd.array(df["decade_start"], dtype="Int64")

    before = len(df)
    df = df[df["genre"].notna() & (df["genre"] != "")]
    discarded = before - len(df)

    if discarded > 0:
        logger.warning(f"{discarded} artistas descartados por falta de gênero")

    return df[["artist_id", "name", "genre", "country", "begin_year", "decade_start"]]


def _extract_year(life_span: dict) -> int | None:
    if not isinstance(life_span, dict):
        return None
    begin = life_span.get("begin")
    if not begin:
        return None
    try:
        return int(str(begin)[:4])
    except (ValueError, TypeError):
        return None


def _to_decade(year: int | None) -> int | None:
    if year is None:
        return None
    return (year // 10) * 10