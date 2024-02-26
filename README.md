# Report Microbiologia

## Indice

- [Report Microbiologia](#report-microbiologia)
  - [Indice](#indice)
  - [Descrizione](#descrizione)
  - [Setup iniziale](#setup-iniziale)
  - [Utilizzo](#utilizzo)
    - [Opzioni](#opzioni)
  - [Correzioni manuali al database](#correzioni-manuali-al-database)
  - [Istruzioni](#istruzioni)
    - [`instructions`](#instructions)
    - [`rate_instructions`](#rate_instructions)

## Descrizione

Tool per analizzare l'export dei dati microbiologici di Mercurio.
Permette di elencare i microorganismi isolati con eventuale meccanismo di resistenza ed altre informazioni utili. Inoltre, fa un calcolo del numero complessivo di isolati e resistenti con relativa percentuale.
Le istruzioni su cosa e come calcolare sono contenute nel file instructions.py che può essere modificato.
Implementa inoltre dei meccanismi di caching che tengono traccia dei file analizzati e li ricalcolano solo se i file o il meccanismo di analisi cambia.

© 2024 - Zeno Dalla Valle

Si ringraziano il dott M. Moro, P. Rizzi, S. Carletti e M. Tonelli per il supporto e la collaborazione.

## Setup iniziale

1. Installare Python 3.10 o superiore
2. [*Opzionale ma fortemente consigliato*] Creare un ambiente virtuale e attivarlo `python -m venv env` e
   `env\Scripts\activate` se si è su Windows o `. env/bin/activate` se si è su Linux/Mac
3. Installare le dipendenze con `pip install -r requirements.txt`

## Utilizzo

1. Creare cartella "data" e inserire al suo interno i file .csv export di Mercurio (i file devono essere l'export mensile, consigliato dal primo giorno del mese al decimo giorno del mese successivo) avendo cura di nominarli `ANNO-MESE.csv` con ANNO di due cifre e MESE di due cifre es. `23-05.csv` per il mese di maggio 2023.
2. Attivare l'ambiente virtuale se si è deciso di crearlo con `env\Scripts\activate` se si è su Windows o `. env/bin/activate` se si è su Linux/Mac
3. Eseguire il programma con `python analyze.py [-h] [--month MONTH] [--output-folder OUTPUT_FOLDER] [--drop-column DROP_COLUMN] [--days-cutoff DAYS_CUTOFF] [--days-hospitalization DAYS_HOSPITALIZATION] [--n-admissions N_ADMISSIONS] year`

L'unico argomento obbligatorio è l'anno, mentre gli altri sono opzionali, incluso il mese. Se non viene specificato il mese lo script considera tutto l'anno come periodo di analisi.

### Opzioni

- `-h`, `--help` show the help message
- `--month MONTH`, `-m MONTH`

  Il mese da analizzare, se non specificato verranno analizzati tutti i mesi dell'anno. (default: `None`)

- `--output-folder OUTPUT_FOLDER`, `-o OUTPUT_FOLDER`

  La cartella in cui salvare i file excel (se non esiste verrà creata). Non supporta la creazione di cartelle annidate. (default: `out`)

- `--drop-column DROP_COLUMN`

  La colonna del file excel in cui scrivere i motivi per cui un isolato è stato scartato (se vuota significa che l'osservazione è valida ai fini del conteggio). (default: `to_drop`)

- `--default-days-cutoff DEFAULT_DAYS_CUTOFF`

  Il numero di giorni da considerare per il calcolo dei duplicati, se non specificato nel file instructions.py. (default: `30`)

- `--days-hospitalization DAYS_HOSPITALIZATION`, `-d DAYS_HOSPITALIZATION`

  Il numero di giorni da considerare per il calcolo dei tassi di isolamenti per 10.000 giornate di degenza. Se assente questi non verranno calcolati. (default: `None`)

- `--n-admissions N_ADMISSIONS`, `-n N_ADMISSIONS`

  Il numero di ricoveri (o pazienti) da considerare per il calcolo dei tassi di isolamenti per 1.000 ricoveri (o pazienti). Se assente questi non verranno calcolati. (default: `None`)

## Correzioni manuali al database

Tramite il file `manual_db_adds.xlsx` è possibile aggiungere manualmente delle righe al database. Il file deve essere compilato seguendo il modello che viene fornito con il programma e permette di aggiungere solo dei risultati per gli antibiotici testati. In sostanza non è possibile aggiungere un nuovo isolato, ma solo dei risultati per un microorganismo già isolato da quel paziente associato a quel preciso numero di richiesta. Questo è dovuto al fatto che per ricavare le informazioni mancanti nel file manual_db_adds.xlsx le osservazioni aggiunte vengono matchate con le osservazioni già presenti nel database secondo i campi: "cognome_paziente", "nome_paziente", "id_richiesta", "id_microbo". Se non viene trovata nessuna corrispondenza l'osservazione viene scartata.

**Attenzione, questo file dopo la compilazione conterrà informazioni sensibili e non deve essere condiviso.**

## Istruzioni

Il file `instructions.py` raccoglie le istruzioni sui calcoli che lo script deve eseguire.

Il file finale deve contenere due variabili: `instructions` e `rate_instructions`.

### `instructions`

Questa lista contiene tutte le istruzioni per il calcolo dei dati. Ogni istruzione è un oggetto di tipo `utils.instructions._instructions`. Per essere inzializzato richiede i seguenti argomenti posizionali:

- `tag`: il tag del materiale da analizzare es. _sorv_pass_
- `descrizione`: la descrizione del materiale da analizzare es. _Sorveglianza passiva_
- `gruppo_microbo_id`: l'id del gruppo di microbi da analizzare es. _citspp_
- `descrizione_gruppo_microbo`: la descrizione del gruppo di microbi da analizzare es. _Citrobacter spp_

E i seguenti argomenti opzionali:

- `cutoff_repeat_days`: il numero di giorni da considerare per il calcolo dei duplicati, se non specificato verrà preso il valore di default.

### `rate_instructions`

**I tassi vengono calcolati escludendo il PS e le attività MAC.**

Questa lista contiene tutte le istruzioni per il calcolo dei tassi di isolamenti. Ogni istruzione è un oggetto di tipo `utils.instructions._rate_instructions`. Per essere inzializzato richiede i seguenti argomenti posizionali:

- `tag`: il tag del materiale da analizzare es. _sangue_
- `descrizione`: la descrizione del materiale da analizzare es. _Sangue (noPS, noMAC)_
- `id_gruppo_microbi`: l'id del gruppo di microbi da analizzare es. _citspp_. In alternativa si può passare una lista degli id di gruppi di microbi da analizzare es. _["acibcx", "entspp", "esccol", "kleoxy", "klespp", "klepne", "prospp", "pseaer", "psespp", "staaur"]_. In questo caso il tasso verrà calcolato sommando gli isolamenti dei gruppi di microbi specificati, mentre le ripetizioni verranno comunque calcolate sul singolo microbo. Ad esempio se un pazientie ha isolato 2 Citrobacter spp a distanza minore del valore di cutoff e 1 Klebsiella pneumoniae il valore dato da quel paziente per il calcolo del tasso sarà 2.
- `descrizione_gruppo_microbi`: la descrizione del gruppo di microbi da analizzare es. _Batteriemie da MDRO (qualunque resistenza)_
- `select_fn`: la funzione di selezione dei dati da considerare per il calcolo del tasso. Deve essere una funzione che prende in input un DataFrame contenente tutti gli isolati (anche i ripetuti che verranno eliminati successivamente) con le colonne sotto riportate e restituisce una serie su cui poi viene applicata la funzione `sum`. Es. _`lambda df: df.resistente.astype(bool)`_ per calcolare il tasso di isolamenti resistenti (qualunque resistenza).

E i seguenti argomenti opzionali:

- `cutoff_repeat_days`: il numero di giorni da considerare per il calcolo dei duplicati, se non specificato verrà preso il valore di default.

**Colonne del DataFrame passato alla funzione di selezione:**
id_richiesta tag tags data_prelievo nome_reparto id_gruppo_microbo nome_gruppo_microbo nome_microbo resistente n_resistenze to_drop

- `id_richiesta`: l'id della richiesta
- `tag`: il tag richiesto dall'istruzione
- `tags`: i tag del materiale oggetto dell'isolamento
- `data_prelievo`: la data del prelievo
- `nome_reparto`: il nome del reparto in cui è stato prelevato il campione
- `id_gruppo_microbo`: l'id del gruppo di microbi
- `nome_gruppo_microbo`: il nome del gruppo di microbi
- `nome_microbo`: il nome del microbo
- `resistente`: le resistenze del microbo separate da `|` es. _ESBL|MDR_. Attenzione: se il microbo non è resistente il campo è un testo vuoto, se il microbo non prevede il calcolo della resistenza il campo è `NA`.
- `n_resistenze`: il numero di resistenze del microbo.
