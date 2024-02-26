import itertools
import pandas as pd


def _pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


if not hasattr(itertools, "pairwise"):
    setattr(itertools, "pairwise", _pairwise)


def _drop_duplicated_resistance_wise(df, days_cutoff=30, drop_column="to_drop"):
    """drop duplicates keeping the first resistant in chronological order"""
    df = df.sort_values("data_prelievo")
    # Prima di tutto eliminiamo i duplicati resistenti tenendo i primi in ordine cronologico
    next_iteration = True
    not_drop_df = df[df[drop_column].isnull()]
    while next_iteration and not_drop_df.resistente.astype(bool).sum() > 0:
        next_iteration = False
        indexes, rows = list(
            zip(*not_drop_df[not_drop_df.resistente.astype(bool)].iterrows())
        )
        for (previous_index, previous_row), (index, row) in itertools.pairwise(
            zip(indexes, rows)
        ):
            if (row.data_prelievo - previous_row.data_prelievo).days < days_cutoff:
                if row.n_resistenze > previous_row.n_resistenze:
                    df.loc[previous_index, drop_column] = (
                        f'Duplicato di id_richiesta: {row.id_richiesta} (data prelievo: {row.data_prelievo.strftime("%Y-%m-%d")}), che ha più resistenze'
                    )
                elif row.n_resistenze < previous_row.n_resistenze:
                    df.loc[index, drop_column] = (
                        f'Duplicato di id_richiesta: {previous_row.id_richiesta} (data prelievo: {previous_row.data_prelievo.strftime("%Y-%m-%d")}), che aveva più resistenze'
                    )
                else:
                    df.loc[index, drop_column] = (
                        f'Duplicato di id_richiesta: {previous_row.id_richiesta} (data prelievo: {previous_row.data_prelievo.strftime("%Y-%m-%d")}), entrambi con lo stesso numero di resistenze'
                    )
                next_iteration = True
            not_drop_df = df[df[drop_column].isnull()]

    # Ora eliminiamo tutti i duplicati tenendo i primi resistenti in ordine cronologico, se non ci sono resistenti teniamo i primi in ordine cronologico
    next_iteration = True
    while next_iteration:
        next_iteration = False
        indexes, rows = list(zip(*not_drop_df.iterrows()))
        for (previous_index, previous_row), (index, row) in itertools.pairwise(
            zip(indexes, rows)
        ):
            if (row.data_prelievo - previous_row.data_prelievo).days < days_cutoff:
                if previous_row.resistente and row.resistente:
                    raise ValueError(
                        "There should not be two consecutive resistant rows"
                    )
                elif previous_row.resistente and not row.resistente:
                    df.loc[index, drop_column] = (
                        f'Duplicato di id_richiesta: {previous_row.id_richiesta} (data prelievo: {previous_row.data_prelievo.strftime("%Y-%m-%d")}), che era resistente'
                    )
                elif not previous_row.resistente and row.resistente:
                    df.loc[previous_index, drop_column] = (
                        f'Duplicato di id_richiesta: {row.id_richiesta} (data prelievo: {row.data_prelievo.strftime("%Y-%m-%d")}), che è/sarà resistente'
                    )
                else:
                    df.loc[index, drop_column] = (
                        f'Duplicato di id_richiesta: {previous_row.id_richiesta} (data prelievo: {previous_row.data_prelievo.strftime("%Y-%m-%d")}), entrambi non resistenti'
                    )
                next_iteration = True
            not_drop_df = df[df[drop_column].isnull()]
    return df


def filter_query_repeated_isolation_in_patients_lt_1_month_resistance_wise(
    df,
    days_cutoff=30,
    drop_column="to_drop",
):
    df = df.copy()
    df[drop_column] = pd.NA
    group_cols = ["cognome_paziente", "nome_paziente", "data_nascita"]
    return (
        df.groupby(group_cols, as_index=False)
        .apply(
            _drop_duplicated_resistance_wise,
            days_cutoff=days_cutoff,
            drop_column=drop_column,
        )
        .reset_index(drop=True)
    )


def _drop_duplicated_no_resistance(df, days_cutoff=30, drop_column="to_drop"):
    """drop duplicates keeping the first in chronological order"""
    df = df.sort_values("data_prelievo")
    # eliminiamo tutti i duplicati tenendo i primi in ordine cronologico
    next_iteration = True
    not_drop_df = df[df[drop_column].isnull()]
    while next_iteration:
        next_iteration = False
        indexes, rows = list(zip(*not_drop_df.iterrows()))
        for (previous_index, previous_row), (index, row) in itertools.pairwise(
            zip(indexes, rows)
        ):
            if (row.data_prelievo - previous_row.data_prelievo).days < days_cutoff:
                df.loc[index, drop_column] = (
                    f'Duplicato di id_richiesta: {previous_row.id_richiesta} (data prelievo: {previous_row.data_prelievo.strftime("%Y-%m-%d")})'
                )
                next_iteration = True
            not_drop_df = df[df[drop_column].isnull()]
    return df


def filter_query_repeated_isolation_in_patients_lt_1_month_no_resistance(
    df, days_cutoff=30, drop_column="to_drop"
):
    df = df.copy()
    df[drop_column] = pd.NA
    group_cols = ["cognome_paziente", "nome_paziente", "data_nascita"]
    return (
        df.groupby(group_cols, as_index=False)
        .apply(
            _drop_duplicated_no_resistance,
            days_cutoff=days_cutoff,
            drop_column=drop_column,
        )
        .reset_index(drop=True)
    )
