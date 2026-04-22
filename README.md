# Artist Recommender Pipeline

Pipeline ETL que extrai dados reais de artistas via [MusicBrainz API](https://musicbrainz.org/doc/MusicBrainz_API), armazena no Supabase e serve recomendações de artistas similares via dashboard Streamlit.

## Como funciona

Digite um artista → o sistema encontra outros com mesmo gênero, época próxima (±10 anos) e preferencialmente mesmo país.

**Sem machine learning. Lógica pura em SQL + pandas.**

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Extração | Python + requests (MusicBrainz API) |
| Transformação | pandas |
| Armazenamento | Supabase (PostgreSQL) |
| Dashboard | Streamlit |
| CI/CD | GitHub Actions |
| Containerização | Docker |
| Testes | pytest |

## Setup local

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/artist-recommender.git
cd artist-recommender

# 2. Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais do Supabase

# 5. Execute o pipeline
python scripts/run_pipeline.py

# 6. Suba o dashboard
streamlit run dashboard/app.py
```

## Com Docker

```bash
docker-compose up pipeline   # executa o ETL
docker-compose up dashboard  # sobe o dashboard em localhost:8501
```

## Governança

Ver [GOVERNANCE.md](GOVERNANCE.md) para política de qualidade de dados, SLA e change management.
