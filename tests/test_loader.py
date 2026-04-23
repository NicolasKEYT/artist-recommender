import pytest
import pandas as pd
from unittest.mock import MagicMock, patch


def make_df():
    return pd.DataFrame([{
        "artist_id": "abc123",
        "name": "Test Artist",
        "genre": "rock",
        "country": "US",
        "begin_year": 1990,
        "decade_start": 1990,
    }])


def test_load_calls_upsert():
    with patch("src.loader.supabase_loader.get_client") as mock_client:
        mock_table = MagicMock()
        mock_client.return_value.table.return_value = mock_table
        mock_table.upsert.return_value.execute.return_value = None

        from src.loader.supabase_loader import load
        stats = load(make_df())

        assert stats["loaded"] == 1
        mock_table.upsert.assert_called_once()


def test_load_returns_correct_count():
    with patch("src.loader.supabase_loader.get_client") as mock_client:
        mock_table = MagicMock()
        mock_client.return_value.table.return_value = mock_table
        mock_table.upsert.return_value.execute.return_value = None

        from src.loader.supabase_loader import load
        df = make_df()
        stats = load(df)

        assert stats["loaded"] == len(df)