import pytest
import pandas as pd
from src.transformer.normalizer import normalize, _extract_year, _to_decade


def make_artist(name="Test Artist", mbid="123", genre="rock", listeners=50000, country=None, begin="1990-01-01"):
    return {
        "name": name,
        "mbid": mbid,
        "_genre": genre,
        "listeners": listeners,
        "_country": country,
        "_life_span": {"begin": begin} if begin else {},
    }


def test_normalize_returns_dataframe():
    artists = [make_artist()]
    df = normalize(artists)
    assert isinstance(df, pd.DataFrame)


def test_normalize_correct_columns():
    artists = [make_artist()]
    df = normalize(artists)
    assert set(df.columns) == {"artist_id", "name", "genre", "country", "begin_year", "decade_start"}


def test_normalize_discards_empty_genre():
    artists = [make_artist(genre="")]
    df = normalize(artists)
    assert len(df) == 0


def test_normalize_deduplicates():
    artists = [make_artist(mbid="abc"), make_artist(mbid="abc")]
    df = normalize(artists)
    assert len(df) == 1


def test_extract_year_valid():
    assert _extract_year({"begin": "1994-05-01"}) == 1994


def test_extract_year_none():
    assert _extract_year({}) is None
    assert _extract_year(None) is None


def test_to_decade():
    assert _to_decade(1994) == 1990
    assert _to_decade(2001) == 2000
    assert _to_decade(None) is None