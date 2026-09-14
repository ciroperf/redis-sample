# Redis: cos'e' e quando conviene

Questo documento da' il contesto per interpretare i numeri e i grafici
prodotti da questo repository (`benchmark/` e `charts/`): cos'e' Redis, come
funziona, quando ha senso metterlo in mezzo come cache e quando invece
aggiunge solo complessita' senza benefici reali.

## Cos'e' Redis e come funziona

Redis (**RE**mote **DI**ctionary **S**erver) e' un data store **in-memory**:
tiene i dati in RAM invece che su disco, il che lo rende ordini di grandezza
piu' veloce di un database relazionale o di una chiamata a un sistema
"lento" (una query complessa, una join costosa, una chiamata a un servizio
esterno con rate limit).

Punti chiave:

- **Strutture dati, non solo chiave/valore**: oltre alle stringhe semplici
  (quelle usate in questo repo, via `redis-py`), Redis espone liste, set,
  hash, sorted set, stream. Questo lo rende utile anche per casi diversi
  dal semplice caching (contatori, code, classifiche, rate limiting).
- **Single-threaded per i comandi**: ogni comando viene eseguito in modo
  atomico, senza bisogno di lock espliciti lato applicazione per operazioni
  singole.
- **TTL nativo**: ogni chiave puo' avere una scadenza (`EXPIRE`), che e'
  esattamente il meccanismo usato dall'endpoint `/data/cached` di questo
  repo per invalidare i dati dopo 30 secondi senza doverlo fare a mano.
- **Persistenza opzionale**: essendo in-memory, i dati si perdono se il
  processo muore, a meno di abilitare la persistenza su disco (RDB:
  snapshot periodici; AOF: log di ogni scrittura, replay all'avvio). Per un
  uso puramente come cache la persistenza e' spesso superflua: se i dati
  spariscono, si ricalcolano dalla sorgente originale (quella "lenta") alla
  richiesta successiva. Diventa importante solo se si usa Redis come store
  primario (non il caso di questo repo).

## Quando conviene usarlo come cache

Redis come cache paga quando valgono insieme queste condizioni:

- **Letture molto piu' frequenti delle scritture** (read-heavy): lo stesso
  dato viene richiesto tante volte tra una modifica e l'altra, quindi il
  costo di calcolarlo una volta si ammortizza su molte letture dalla cache.
- **Dati costosi da ricalcolare**: query pesanti, join su tabelle grandi,
  chiamate a servizi esterni lenti o con costo per chiamata. E' esattamente
  quello che l'endpoint `/data/nocache` di questo repo simula con una
  latenza artificiale di 50-150ms.
- **Tolleranza a dati leggermente stale**: se va bene servire un valore
  vecchio di qualche secondo (o dei 30s di TTL usati qui) pur di guadagnare
  in velocita', la cache e' un buon compromesso. Il TTL definisce quanto
  "vecchio" puo' essere il dato prima di essere ricalcolato.

In questi casi il guadagno e' misurabile: nel benchmark di questo repo la
differenza tra `/data/nocache` e `/data/cached` (con `REDIS_URL` reale
configurata) e' di uno o due ordini di grandezza sul tempo di risposta dopo
il primo accesso (si veda `README.md`, sezione "Benchmark e grafici").

## Quando NON conviene

Aggiungere una cache non e' mai gratis: introduce un componente in piu' da
gestire, monitorare e tenere disponibile, e sposta un problema di
performance in un problema di consistenza. Non conviene quando:

- **I dati cambiano a ogni scrittura o quasi**: se il tasso di scrittura e'
  vicino a quello di lettura, la cache viene invalidata cosi' spesso che il
  suo hit rate crolla e il costo di mantenerla (scritture doppie, gestione
  invalidazione) supera il beneficio.
- **Serve consistenza forte**: se il sistema non puo' tollerare di leggere
  un dato non aggiornato nemmeno per una manciata di secondi (es. saldi
  finanziari, stock in tempo reale su vendite critiche), una cache con TTL
  introduce una finestra di incoerenza che va gestita esplicitamente
  (invalidazione attiva, write-through), aumentando la complessita' invece
  di ridurla.
- **Il working set non entra in RAM**: Redis tiene tutto in memoria, quindi
  la dimensione della cache e' vincolata alla RAM disponibile sull'istanza.
  Se l'insieme di dati "caldi" (quelli effettivamente riletti spesso) e'
  piu' grande della RAM disponibile, si finisce con eviction continua
  (Redis scarta chiavi per far spazio) e un hit rate basso, che vanifica il
  vantaggio della cache pur pagandone il costo operativo.

In questi scenari, il tempo speso a introdurre e mantenere Redis rischia di
non tradursi in un miglioramento visibile nei numeri, o addirittura di
peggiorare l'affidabilita' del sistema (un componente in piu' che puo'
fallire).

## Costi e complessita' operativa (Azure Cache for Redis)

Il Terraform in `terraform/` di questo repo provisiona un'istanza **Azure
Cache for Redis** in tier **Basic** (si veda `terraform/main.tf` e
`terraform/variables.tf`), scelta deliberatamente per il confronto di
performance in questo repo, non come riferimento per la produzione:

- **Basic**: singola istanza, nessuna replica, **nessuna SLA di alta
  affidabilita'**. Se il nodo va giu' o viene riavviato per manutenzione, la
  cache non e' disponibile finche' non torna su. Adatta solo a
  sviluppo/test o a cache non critiche (se Redis sparisce, l'applicazione
  deve saper ricadere sulla sorgente dati originale, come fa
  `/data/cached` in questo repo quando `REDIS_URL` non e' impostata).
- **Standard**: aggiunge una replica in alta disponibilita' con failover
  automatico, a un costo circa doppio rispetto a Basic per la stessa
  dimensione.
- **Premium**: aggiunge clustering (per superare il limite di RAM di un
  singolo nodo), persistenza su disco, VNET injection, geo-replicazione e
  zone di disponibilita'; e' il tier richiesto per carichi di produzione
  seri, con un costo significativamente piu' alto degli altri due.

A questi costi diretti si aggiunge la complessita' operativa: un'istanza
Redis in produzione va monitorata (memoria usata, eviction, hit rate,
latenza), va gestita per gli aggiornamenti/patch, e va considerata come
ulteriore punto di failure nella catena di dipendenze dell'applicazione.
Questo e' il costo che va confrontato con il guadagno di performance
misurato nel benchmark, per decidere se, nel proprio contesto, ne vale la
pena.

## Evidenza empirica: i grafici del benchmark

I numeri di questa sezione non sono astratti: sono generati dal benchmark
incluso nel repo. Dopo aver eseguito

```bash
python benchmark/run_benchmark.py
python charts/generate_charts.py
```

i grafici KPI vengono scritti in `charts/output/` (cartella non versionata,
rigenerata a ogni esecuzione):

- `charts/output/mean_response_time.png` — tempo medio di risposta, cached
  vs nocache: mostra il guadagno "a regime" della cache.
- `charts/output/percentiles.png` — percentili p50/p95/p99 per i due
  endpoint: utile per capire non solo il caso medio ma anche la coda
  (quanto puo' essere lento il caso peggiore).
- `charts/output/response_time_distribution.png` — distribuzione dei tempi
  di risposta: rende visibile la differenza di forma tra una distribuzione
  dominata dalla latenza artificiale della sorgente lenta e una dominata
  dai tempi di risposta di Redis.

Per un esempio gia' pronto (senza dover eseguire il benchmark) si veda
`docs/img/mean_response_time_example.png`, linkato anche dal `README.md`
principale.
