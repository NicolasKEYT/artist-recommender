import pandas as pd
import logging

logger = logging.getLogger(__name__)

VALID_GENRES = {
    "rock", "pop", "jazz", "metal", "hip-hop",
    "electronic", "classical", "blues", "reggae", "punk",
    "country", "r&b", "soul", "folk", "latin",
    "alternative", "indie", "funk", "gospel", "disco"
}


def normalize(artists_raw: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(artists_raw)

    df["artist_id"] = df["mbid"].where(df["mbid"] != "", other=None)
    df["artist_id"] = df["artist_id"].fillna(df["name"].str.lower().str.strip())

    df["name"] = df["name"].str.strip()
    df["genre"] = df["_genre"]
    df["listeners"] = pd.to_numeric(df["listeners"], errors="coerce")
    df["country"] = df["_country"].where(df["_country"].notna(), other=None)
    df["begin_year"] = df["_life_span"].apply(_extract_year)
    df["decade_start"] = df["begin_year"].apply(_to_decade)

    df["begin_year"] = pd.array(df["begin_year"], dtype="Int64")
    df["decade_start"] = pd.array(df["decade_start"], dtype="Int64")

    before = len(df)
    df = df[df["genre"].notna() & (df["genre"] != "")]
    df = df.drop_duplicates(subset="artist_id", keep="first")
    discarded = before - len(df)

    if discarded > 0:
        logger.warning(f"{discarded} artistas descartados ou duplicados")

    return df[["artist_id", "name", "genre", "country", "begin_year", "decade_start"]]


def _extract_year(life_span) -> int | None:
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