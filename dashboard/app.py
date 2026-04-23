import os
import pandas as pd
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Artist Recommender", page_icon="🎵", layout="centered")


@st.cache_resource
def get_client():
    return create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


@st.cache_data(ttl=3600)
def get_all_artists() -> pd.DataFrame:
    client = get_client()
    response = client.table("artists").select("*").execute()
    return pd.DataFrame(response.data)


def recommend(df: pd.DataFrame, artist_name: str, n: int = 10) -> pd.DataFrame:
    name_lower = artist_name.strip().lower()
    match = df[df["name"].str.lower() == name_lower]

    if match.empty:
        return pd.DataFrame()

    target = match.iloc[0]

    candidates = df[df["name"].str.lower() != name_lower].copy()

    def score(row):
        s = 0
        if row["genre"] == target["genre"]:
            s += 50
        if row["country"] == target["country"] and pd.notna(target["country"]):
            s += 30
        if pd.notna(row["decade_start"]) and pd.notna(target["decade_start"]):
            if abs(row["decade_start"] - target["decade_start"]) <= 10:
                s += 20
        return s

    candidates["score"] = candidates.apply(score, axis=1)
    candidates = candidates[candidates["score"] > 0]
    candidates = candidates[candidates["genre"] == target["genre"]]

    return candidates.sort_values("score", ascending=False).head(n)


# --- UI ---
st.title("🎵 Artist Recommender")
st.caption("Digite um artista e descubra outros similares por gênero, época e país.")

df = get_all_artists()

artist_input = st.text_input("Nome do artista", placeholder="ex: Nirvana, Miles Davis, Bob Marley")

if artist_input:
    results = recommend(df, artist_input)

    if results.empty:
        st.warning("Artista não encontrado no banco. Tente outro nome.")
    else:
        target = df[df["name"].str.lower() == artist_input.strip().lower()].iloc[0]
        st.markdown(f"**Gênero:** {target['genre']} · **País:** {target['country'] or 'N/A'} · **Década:** {int(target['decade_start']) if pd.notna(target['decade_start']) else 'N/A'}s")
        st.divider()

        for _, row in results.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{row['name']}**")
                st.caption(f"{row['genre']} · {row['country'] or 'N/A'} · {int(row['decade_start']) if pd.notna(row['decade_start']) else 'N/A'}s")
            with col2:
                st.metric("Score", int(row["score"]))