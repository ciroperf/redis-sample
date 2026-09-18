# redis-sample

Dimostra con numeri i vantaggi/svantaggi del caching Redis: API con e senza
cache su un catalogo prodotti reale (DB), benchmark strutturato, grafici
KPI, Terraform per Azure Cache for Redis e Azure Database for PostgreSQL.

Questo file viene letto a ogni run dell'agente. Tienilo sotto le 40 righe.

## Stack

- Python 3.12, FastAPI + redis-py, SQLAlchemy per il DB (`DATABASE_URL`)
- Terraform, provider `azurerm`
- Test: `pytest` (DB reale su SQLite temporaneo, `fakeredis` per la cache)
- Avvio locale: `uvicorn app.main:app --reload`

## Regole

1. Mai push su `main`. Branch, PR, stop.
2. Un compito, una PR. Niente refactor non richiesti.
3. Se il compito e' ambiguo: commenta la domanda sull'issue e fermati.
4. Leggi in modo mirato con Grep e Glob. Non aprire `node_modules`, `dist`,
   `build`, `.next`, `bin`, `obj`, `.terraform`, `*.lock`.
5. Nessun segreto nel codice, nemmeno negli esempi. Le credenziali Azure
   passano per variabili d'ambiente, mai hardcoded nei `.tf`.
6. Nessuna dipendenza nuova senza scriverne il motivo nella PR.

## Convenzioni

- Codice e identificatori in inglese, commenti in italiano.
- Commit in forma imperativa, una riga.
- `app/` l'API dimostrativa e il layer DB, `db/` schema e seed SQL del
  catalogo, `benchmark/` raccoglie i dati in CSV, `charts/` genera i
  grafici a partire dal CSV, `terraform/` l'infra Azure, `docs/` le guide
  su Redis e sul collegamento al DB.

## Fatto quando

Una PR e' pronta se: `pytest` passa, il README riflette le novita', e
un'immagine o un output di esempio mostra il risultato.
