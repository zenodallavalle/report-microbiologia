import json
import os
from typing import Iterable, Optional, Union
import pandas as pd
from collections import Counter
import hashlib


_utils_listdir_to_monitor = [
    ["utils", f]
    for f in os.listdir("utils")
    if not (os.path.isdir(f) or f.startswith("__"))
]
_additional_to_monitor = []

_monitor_cache_files = _utils_listdir_to_monitor + _additional_to_monitor

_CURRENT_VERSION_HASHES = {}
_CACHED_VERSION_HASHES = {}


def generate_excel_output_filename(excel_output_folder_name, year, month):
    os.makedirs(excel_output_folder_name, exist_ok=True)
    return os.path.join(
        excel_output_folder_name,
        f"{year}-{month:02d}.xlsx" if month is not None else f"{year}-all.xlsx",
    )


def check_parameters(**kwargs):
    month = kwargs.get("month")
    year = kwargs.get("year")
    if month is not None:
        if not 1 <= month <= 12:
            raise ValueError("Il mese deve essere compreso tra 1 e 12")
    if year < 1900:
        raise ValueError("L'anno deve essere maggiore di 1900")
    if year > pd.Timestamp.now().year:
        raise ValueError("L'anno non può essere maggiore dell'anno corrente")


def check_total_df(total_df):
    if total_df.empty:
        raise ValueError("Nessun dato presente!")
    assert (
        not total_df.data_prelievo.isnull().sum()
    ), "data_prelievo contains null values"
    assert not (
        total_df[total_df.id_gruppo_microbo == "esccol"]
        .groupby(["id_esame", "id_gruppo_microbo", "nome_gruppo_microbo"])
        .esbl.nunique()
        != 1
    ).any(), "esbl is not unique for esccol"
    assert not (
        total_df.groupby(
            ["id_esame", "id_gruppo_microbo", "nome_gruppo_microbo"]
        ).data_prelievo.nunique()
        != 1
    ).any(), "data_prelievo is not unique"


def _check_current_version_hash():
    ret = {}
    for path, file in _monitor_cache_files:
        with open(os.path.join(path, file), "rb") as f:
            file_hash = hashlib.md5(
                f.read().decode("utf-8", errors="ignore").encode("utf-8")
            ).hexdigest()
            ret[file] = file_hash
    return ret


def _get_cached_version():
    try:
        with open(os.path.join("_cached_data", "version.json")) as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading version.json: {e}")
        return {}


def _get_hash_for_file(file):
    try:
        with open(file, "rb") as f:
            return hashlib.md5(
                f.read().decode("utf-8", errors="ignore").encode("utf-8")
            ).hexdigest()
    except Exception as e:
        print(f'Error loading file "{file}": {e}')
        return None


def _check_cached_version(silent=False):
    global _CURRENT_VERSION_HASHES, _CACHED_VERSION_HASHES

    _CURRENT_VERSION_HASHES = _check_current_version_hash()
    _CACHED_VERSION_HASHES = _get_cached_version()

    for filename, hash in _CURRENT_VERSION_HASHES.items():
        if filename not in _CACHED_VERSION_HASHES:
            if not silent:
                print(
                    f"File {filename} not in cached version, reprocess all files and update version.json"
                )
            return False
        if hash != _CACHED_VERSION_HASHES[filename]:
            if not silent:
                print(
                    f"File {filename} has different hash, reprocess all files and update version.json"
                )
            return False
    return True


def _update_cached_version():
    global _CURRENT_VERSION_HASHES

    with open(os.path.join("_cached_data", "version.json"), "w") as f:
        json.dump(_CURRENT_VERSION_HASHES, f)


def _generate_csv_legend_path(file: str) -> Union[str, os.PathLike]:
    abs_folder = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(abs_folder, file)


columns_mapper = pd.read_csv(
    _generate_csv_legend_path("columns_mapper.csv"), index_col=0
).valore
tags_materiale_mapper = pd.read_csv(
    _generate_csv_legend_path("materiale_mapper.csv"), index_col=0
).tags.str.split("|")
microbo_mapper = pd.read_csv(
    _generate_csv_legend_path("microbo_mapper.csv"), index_col=0
)


def _safe_decode(x: bytes):
    try:
        return x.decode("utf-8")
    except:
        return x.decode("windows-1252")


def _custom_reader(path):
    def gen_summed_lines(lines, i, j):
        return "".join([lines[i + jj] for jj in range(j)])

    with open(path, "rb") as f:
        lines = f.readlines()
    try:
        lines = list(map(_safe_decode, lines))
    except UnicodeDecodeError:
        print("Error decoding file: {}".format(path))

    c = Counter(map(lambda x: len(x.split(",")), lines))
    n_expected_fields = c.most_common(1)[0][0]
    i = 0
    while i < len(lines):
        yielded = False
        if len(lines[i].split(",")) == n_expected_fields:
            yield lines[i].split(",")
            i += 1
            continue
        else:
            j = 1
            summed_line = gen_summed_lines(lines, i, j)
            while len(summed_line.split(",")) <= n_expected_fields:
                if len(summed_line.split(",")) == n_expected_fields:
                    yield summed_line.split(",")
                    yielded = True
                    i += j
                    break
                j += 1
                summed_line = gen_summed_lines(lines, i, j)
        if not yielded:
            try:
                end_tail = lines[i].rsplit(",", 5)[1:]
                start = lines[i].split(",", 30)
                for l in end_tail[::-1]:
                    start[len(start) - 1] = (
                        start[-1].replace(l, "").strip().strip(",").strip()
                    )
                yield start + end_tail
            except Exception as e:
                print(e)
                print(lines[i])
                print("Error")
            i += j


def _read_csv(path: Union[str, os.PathLike], **kwargs):
    lines = [[cell.strip() for cell in line] for line in _custom_reader(path)]
    df = pd.DataFrame(lines[1:], columns=lines[0], **kwargs).replace(
        ["< >", "<null>"], pd.NA
    )
    for col in [
        "Data di nascita",
        "Data di ricovero",
        "Data di dimissione",
        "Data di accettazione",
        "Data di prelievo",
    ]:
        df[col] = pd.to_datetime(df[col])
    return df


def _rename_columns_and_add_missing_info(df):
    df = df.rename(columns=columns_mapper).drop(
        columns=[
            "id_provenienza",
            "nome_provenienza",
        ]
    )
    df["tags"] = df.id_materiale.map(tags_materiale_mapper).fillna("")
    # convert tags from list to string
    df["tags"] = df.tags.map(lambda x: "|".join(x)).str.lower()
    df["id_gruppo_microbo"] = df.id_microbo.map(
        microbo_mapper.id_gruppo_microbo
    ).fillna(df.id_microbo)
    df["nome_gruppo_microbo"] = df.id_microbo.map(
        microbo_mapper.nome_gruppo_microbo
    ).fillna(df.nome_microbo)
    df["esbl"] = df["esbl"].str.contains("POS", case=False, regex=False, na=False)
    df["risultato_quantitativo"] = (
        df["risultato_quantitativo"]
        .str.strip()
        .str.replace("neg", "false", case=False)
        .str.replace("pos", "true", case=False)
    )
    return df


def _process_files(silent=False):
    global _CURRENT_VERSION_HASHES
    """read all csv files in "data" and process them. Process means that columns are renamed, observation are filtered according to month and file is saved as parquet file. Cached file named version.json is evaluated/updated."""
    os.makedirs("_cached_data", exist_ok=True)
    if not _check_cached_version(silent=silent):
        for file in os.listdir("_cached_data"):
            os.remove(os.path.join("_cached_data", file))
    else:
        if not silent:
            print("Cache is coherent with current version. No need to reprocess files.")

    # iterate through all files in data folder
    for file in os.listdir("data"):
        if not file.endswith(".csv") or file.startswith("."):
            continue
        year, month = file.replace(".csv", "").split("-")
        if len(year) == 2:
            year = "20" + year
        month = int(month)
        year = int(year)
        # check if file is already processed
        if os.path.exists(os.path.join("_cached_data", f"{year}-{month}.parquet")):
            actual_file_hash = _get_hash_for_file(os.path.join("data", file))
            try:
                if actual_file_hash == _CACHED_VERSION_HASHES[file]:
                    _CURRENT_VERSION_HASHES[file] = actual_file_hash
                    if not silent:
                        print(f"File {file} already processed, skipping")
                    continue
            except KeyError:
                pass
        if not silent:
            print(f"Processing file {file} as it was not cached or has changed")
        # read csv
        ## FIXME: alcuni valori quantitativi sono registrati con la virgola, con problemi di tabulazione es <=0.25 vs. <=0,25 !!
        df = _read_csv(os.path.join("data", file))
        # rename columns
        df = _rename_columns_and_add_missing_info(df)
        # filter date
        df = df[
            (df.data_prelievo.dt.month == month) & (df.data_prelievo.dt.year == year)
        ]
        # save as parquet
        df.to_parquet(os.path.join("_cached_data", f"{year}-{month}.parquet"))
        # update cached version
        actual_file_hash = _get_hash_for_file(os.path.join("data", file))
        _CURRENT_VERSION_HASHES[file] = actual_file_hash
    _update_cached_version()


def _convert_year_month_to_months(year, month):
    return year * 12 + month


def _convert_months_to_year_month(months):
    y, m = months // 12, months % 12
    if m == 0:
        y -= 1
        m = 12
    return y, m


def _load_manual_db_adds(df):
    manual_db_adds = pd.read_excel(
        "manual_db_adds.xlsx",
        dtype={
            "id_richiesta": str,
            "id_microbo": str,
            "id_antibiotico": str,
            "risultato_quantitativo": str,
        },
    )
    if len(manual_db_adds) == 0:
        return pd.DataFrame()
    print(f'Readed {len(manual_db_adds)} manual_db_adds from "manual_db_adds.xlsx"')
    manual_db_adds = manual_db_adds.reindex(
        columns=[
            "id_richiesta",
            "id_microbo",
            "id_antibiotico",
            "risultato_quantitativo",
        ]
    )
    # Match on cognome_paziente, nome_paziente, id_richiesta, id_microbo in order to inject the id_antibiotico and risultato_quantitativo
    manual_db_adds = pd.merge(
        df.drop(
            columns=[
                "id_antibiotico",
                "nome_antibiotico",
                "risultato_quantitativo",
                "source",
            ]
        ).drop_duplicates(subset=["id_richiesta", "id_microbo"]),
        manual_db_adds,
        on=["id_richiesta", "id_microbo"],
        how="right",
    )
    if (
        manual_db_adds.nome_reparto.isnull().sum() > 0
    ):  # This means that there are some manual_db_adds that were not matched
        print(
            f"WARNING: {manual_db_adds.nome_reparto.isnull().sum()} manual_db_adds were not matched (and so not added), CHECK IF DATA IS CORRECT!\nCould be also due to data not being present in the loaded dataset (e.g. outside the date range)"
        )
    manual_db_adds = manual_db_adds.dropna(subset=["nome_reparto"])
    manual_db_adds["source"] = "manual_db_adds.xlsx"
    return manual_db_adds


def load_data(year, month: Optional[int] = None, silent=False):
    _process_files(silent=silent)
    if month:
        sources = []
        months = _convert_year_month_to_months(year, month)
        for i in range(
            months - 2, months + 3 + 1
        ):  # 12 for margin, 1 for current month
            y, m = _convert_months_to_year_month(i)
            if not os.path.exists(os.path.join("_cached_data", f"{y}-{m}.parquet")):
                if not silent:
                    print(
                        f'File "{y}-{m}.parquet" not found, continuing without it!!!!'
                    )
            else:
                if not silent:
                    print(
                        'File "{}" found, adding it to sources'.format(
                            f"{y}-{m}.parquet"
                        )
                    )
                sources.append(f"{y}-{m}.parquet")
    else:
        sources = []
        months = _convert_year_month_to_months(year, 1)
        for i in range(
            months - 2, months + 12 + 3 + 1
        ):  # 2 for margin, 12 for all months
            y, m = _convert_months_to_year_month(i)
            if not os.path.exists(os.path.join("_cached_data", f"{y}-{m}.parquet")):
                if not silent:
                    print(
                        f'File "{y}-{m}.parquet" not found, continuing without it!!!!'
                    )
            else:
                if not silent:
                    print(
                        'File "{}" found, adding it to sources'.format(
                            f"{y}-{m}.parquet"
                        )
                    )
                sources.append(f"{y}-{m}.parquet")
    # Calculate the bounds of the data using data_prelievo
    if month:
        months = _convert_year_month_to_months(year, month)
        low = _convert_months_to_year_month(months - 2)
        high = _convert_months_to_year_month(months + 3)
    else:
        months = _convert_year_month_to_months(year, 1)
        ## previous and 12 months after
        low = _convert_months_to_year_month(months - 2)
        high = _convert_months_to_year_month(months + 12 + 3)

    def _read(file):
        path = os.path.join("_cached_data", file)
        df = pd.read_parquet(path)
        df["source"] = file
        return df

    df = pd.concat(
        map(_read, sources),
        ignore_index=True,
    )

    # Delete test observations
    df = df[
        ~df.id_richiesta.isin(
            [
                "77441648",
                "77441652",
                "77441942",
                "80851343",
                "80854688",
                "77462443",
                "77462488",
                "77464108",
            ]
        )
    ]
    # Load manual_db_adds
    manual_db_adds = _load_manual_db_adds(df)
    if len(manual_db_adds):
        n_manual_db_adds_not_relevant = (
            ~(  # including the first day of the month
                manual_db_adds.data_prelievo >= f"{low[0]}-{low[1]}-01"
            )
            & (  # excluding the first day of the next month
                manual_db_adds.data_prelievo < f"{high[0]}-{high[1]}-01"
            )
        ).sum()
        manual_db_adds = manual_db_adds[
            (manual_db_adds.data_prelievo >= f"{low[0]}-{low[1]}-01")
            & (manual_db_adds.data_prelievo < f"{high[0]}-{high[1]}-01")
        ]
        print(
            f"Included {len(manual_db_adds)} manual_db_adds ({n_manual_db_adds_not_relevant} not relevant)"
        )
    df = pd.concat([df, manual_db_adds], ignore_index=True)

    df = df[
        (df.data_prelievo >= f"{low[0]}-{low[1]}-01")
        & (df.data_prelievo < f"{high[0]}-{high[1]}-01")
    ]

    df["risultato_quantitativo"] = df.risultato_quantitativo.replace(
        {"false": False, "true": True}
    )
    return df.sort_values("data_prelievo")


def filter_df_for_count(
    df,
    year: int,
    month: Optional[int] = None,
    resistances: Optional[Iterable] = None,
    id_gruppo_microbo: str = None,
    tag: str = None,
    custom_filter_fn=lambda df: df,
    custom_filter_fn_kwargs={},
):
    temp_df = df.copy()
    if id_gruppo_microbo:
        temp_df = temp_df[
            temp_df.id_gruppo_microbo.str.lower() == id_gruppo_microbo.lower()
        ]
    if tag and temp_df.shape[0]:
        temp_df = temp_df[temp_df.tags.str.split("|").apply(lambda tags: tag in tags)]
    if resistances is not None:
        temp_df = temp_df[temp_df.resistente.isin(resistances)]
    temp_df = custom_filter_fn(temp_df, **custom_filter_fn_kwargs)
    # Now restrict to actual year
    temp_df = temp_df[(temp_df.data_prelievo.dt.year == year)]
    # If month is specified, restrict to that month
    if month:
        temp_df = temp_df[(temp_df.data_prelievo.dt.month == month)]
    cols = temp_df.columns.tolist()
    temp_df["tag"] = tag
    temp_df["id_richiesta"] = temp_df["id_richiesta"].astype(int)
    tags_col_index = cols.index("tags")
    cols = cols[:tags_col_index] + ["tag"] + cols[tags_col_index:]
    temp_df = temp_df[cols].copy()
    return temp_df
