import argparse
import sys


from utils import (
    analyze,
    check_parameters,
)

from instructions import instructions, rate_instructions


DEFAULT_EXCEL_OUTPUT_FOLDER_NAME = "out"
DEFAULT_TO_DROP_COLUMN = "to_drop"
DEFAULT_DEFAULT_DAYS_CUTOFF = 30

_description_lines = [
    "Tool per analizzare l'export dei dati microbiologici di Mercurio.",
    "Permette di elencare i microorganismi isolati con eventuale meccanismo di resistenza ed altre informazioni utili. Inoltre, fa un calcolo del numero complessivo di isolati e resistenti con relativa percentuale.",
    "Le istruzioni su cosa e come calcolare sono contenute nel file instructions.py che può essere modificato.",
    "Implementa inoltre dei meccanismi di caching che tengono traccia dei file analizzati e li ricalcolano solo se i file o il meccanismo di analisi cambia.",
    "",
    "© 2024 - Zeno Dalla Valle",
    "Si ringraziano il dott M. Moro, P. Rizzi, S. Carletti e M. Tonelli per il supporto e la collaborazione.",
]


def main():
    args = sys.argv[1:]

    ## Handle command line arguments wisely with the possibility to use --help
    parser = argparse.ArgumentParser(
        description="\n".join(_description_lines),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(dest="year", type=int, help="L'anno da analizzare.")
    parser.add_argument(
        "--month",
        "-m",
        type=int,
        default=None,
        help="Il mese da analizzare, se non specificato verranno analizzati tutti i mesi dell'anno.",
    )
    parser.add_argument(
        "--output-folder",
        "-o",
        type=str,
        default=DEFAULT_EXCEL_OUTPUT_FOLDER_NAME,
        help="La cartella in cui salvare i file excel (se non esiste verrà creata). Non supporta la creazione di cartelle annidate.",
    )
    parser.add_argument(
        "--drop-column",
        type=str,
        default=DEFAULT_TO_DROP_COLUMN,
        help="La colonna del file excel in cui scrivere i motivi per cui un isolato è stato scartato (se vuota significa che l'osservazione è valida ai fini del conteggio).",
    )
    parser.add_argument(
        "--default-days-cutoff",
        type=int,
        default=DEFAULT_DEFAULT_DAYS_CUTOFF,
        help="Il numero di giorni da considerare per il calcolo dei duplicati, se non specificato nel file instructions.py.",
    )
    parser.add_argument(
        "--days-hospitalization",
        "-d",
        type=int,
        default=None,
        help="Il numero di giorni di ospedalizzazione da considerare per il calcolo dei tassi di isolamenti per 10.000 gg di degenza.",
    )
    parser.add_argument(
        "--n-admissions",
        "-n",
        type=int,
        default=None,
        help="Il numero di ricoveri (o pazienti) da considerare per il calcolo dei tassi di isolamenti per 1.000 ricoveri (o pazienti).",
    )
    args = parser.parse_args(args)
    config = vars(args)
    check_parameters(**config)

    # Analyze
    analyze(
        year=config.get("year"),
        month=config.get("month"),
        excel_output_folder_name=config.get("output_folder"),
        drop_column=config.get("drop_column"),
        default_days_cutoff=config.get("default_days_cutoff"),
        instructions=instructions,
        rate_instructions=rate_instructions,
        days_of_hospitalization=config.get("days_hospitalization"),
        number_of_admissions_or_patients=config.get("n_admissions"),
    )


if __name__ == "__main__":
    main()
