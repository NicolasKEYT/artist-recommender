# Governance — Artist Recommender Pipeline

## Política de qualidade de dados

| Regra | Comportamento |
|-------|--------------|
| Artista sem `genre` | **Descartado** — não entra no banco |
| `begin_year` ausente | Aceito — `decade_start` fica `NULL` |
| Nome duplicado (mesmo `artist_id`) | Upsert — atualiza o registro existente |
| País ausente | Aceito — penaliza no score de recomendação |

## SLA de atualização

- Pipeline executa **diariamente às 06:00 UTC** via GitHub Actions
- Falhas geram notificação automática por e-mail (comportamento padrão do GitHub)
- Cada execução registra em log JSON: `timestamp`, `extracted`, `loaded`, `discarded`

## Change management de schema

Qualquer alteração na tabela `artists` requer:

1. PR com descrição do impacto
2. Migration SQL versionada em `scripts/migrations/`
3. Atualização deste arquivo

## Schema atual (v1)

```sql
CREATE TABLE artists (
    artist_id   TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    genre       TEXT NOT NULL,
    country     TEXT,
    begin_year  INTEGER,
    decade_start INTEGER,
    updated_at  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_genre_decade ON artists (genre, decade_start);
CREATE INDEX idx_country ON artists (country);
```
