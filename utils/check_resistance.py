import re
import pandas as pd
from .helper import microbo_mapper


def _cast_float_or_bool(x):
    if pd.isnull(x):
        return x
    if isinstance(x, bool):
        return x
    x = str(x)
    add_major = True if ">" in x or "≥" in x else False

    try:
        return float(re.sub(r">|<|=|≥|≤", "", x).replace(",", ".")) + (
            0.0001 if add_major else 0
        )
    except ValueError:
        return pd.NA


def _extract_value(df, atb_id):
    value_or_values = df.loc[df.id_antibiotico == atb_id, "risultato_quantitativo"]
    if not len(value_or_values):
        return pd.NA
    if len(value_or_values) == 1:
        return _cast_float_or_bool(value_or_values.iloc[0])
    return value_or_values.apply(_cast_float_or_bool).max()


def _check_resistance_and_validity(df):
    # if the function returns NA the observation must be discarded

    if not "id_gruppo_microbo" in df.columns:
        return pd.NA

    resistances = set()
    # Se tampone anale = sorveglianza attiva
    is_sorveglianza_attiva = df.id_materiale.iloc[0] == "TB"
    mdr_value = _extract_value(df, "MDR")
    esbl_value = _extract_value(df, "ESBL")

    kpc_value = _extract_value(df, "KPC")
    kpc_alternative_value = _extract_value(df, "CARBA")
    imp_value = _extract_value(df, "IMP")
    ndm_value = _extract_value(df, "NDM")
    carba_r_value = _extract_value(df, "CARBA-R")
    oxa_value = _extract_value(df, "OXA")
    vim_value = _extract_value(df, "VIM")

    def evaluate_mdr_mech(resistances):
        if (pd.notnull(kpc_value) and kpc_value) or (
            pd.notnull(kpc_alternative_value) and kpc_alternative_value
        ):
            resistances.add("MDR>KPC")
            resistances.add("MDR")
        if pd.notnull(imp_value) and imp_value:
            resistances.add("MDR>IMP")
            resistances.add("MDR")
        if pd.notnull(ndm_value) and ndm_value:
            resistances.add("MDR>NDM")
            resistances.add("MDR")
        if pd.notnull(oxa_value) and oxa_value:
            resistances.add("MDR>OXA-48")
            resistances.add("MDR")
        if pd.notnull(vim_value) and vim_value:
            resistances.add("MDR>VIM")
            resistances.add("MDR")

        # Carba-R is not an MDR, is only a resistance mechanism
        if pd.notnull(carba_r_value) and carba_r_value:
            resistances.add("CAR")

        return resistances

    if df.id_gruppo_microbo.iloc[0] in (
        "esccol",
        "klespp",
        "kleoxy",
        "klepne",
        "klespe",
        "prospp",
        "mormor",
    ):
        if pd.notnull(mdr_value) and mdr_value:
            resistances.add("MDR")
        elif is_sorveglianza_attiva:
            resistances.add("MDR")
        else:
            cefotaxime_value = _extract_value(df, "CTX")
            ceftazidime_value = _extract_value(df, "CAZ")
            if (
                (pd.notnull(esbl_value) and esbl_value)
                or (pd.notnull(cefotaxime_value) and cefotaxime_value > 1)
                or (pd.notnull(ceftazidime_value) and ceftazidime_value > 1)
            ):
                resistances.add("ESBL")

        resistances = evaluate_mdr_mech(resistances)
        return "|".join(resistances)

    elif df.id_gruppo_microbo.iloc[0] in ["pseaer", "psespp", "psepsu"]:
        meropenem_value = _extract_value(df, "MEM")
        imipenem_value = _extract_value(df, "IPM")
        if pd.notnull(mdr_value) and mdr_value:
            resistances.add("MDR")
        elif (pd.notnull(meropenem_value) and meropenem_value > 2) or (
            pd.notnull(imipenem_value) and imipenem_value > 4
        ):
            resistances.add("CAR")
        elif is_sorveglianza_attiva:
            resistances.add("MDR")
        resistances = evaluate_mdr_mech(resistances)
        if "CAR" in resistances and "MDR" in resistances and len(resistances) == 2:
            resistances.remove("MDR")
        return "|".join(resistances)

    elif df.id_gruppo_microbo.iloc[0] == "acibcx":
        if pd.notnull(mdr_value) and mdr_value:
            resistances.add("MDR")
        elif is_sorveglianza_attiva:
            resistances.add("MDR")
        resistances = evaluate_mdr_mech(resistances)
        return "|".join(resistances)

    elif df.id_gruppo_microbo.iloc[0] == "enbaco":
        if pd.notnull(mdr_value) and mdr_value:
            resistances.add("MDR")
        elif is_sorveglianza_attiva:
            resistances.add("MDR")
        resistances = evaluate_mdr_mech(resistances)
        return "|".join(resistances)

    elif df.id_gruppo_microbo.iloc[0] == "citspp":
        if pd.notnull(mdr_value) and mdr_value:
            resistances.add("MDR")
        elif is_sorveglianza_attiva:
            resistances.add("MDR")
        resistances = evaluate_mdr_mech(resistances)
        return "|".join(resistances)

    elif df.id_gruppo_microbo.iloc[0] == "sermar":
        if pd.notnull(mdr_value) and mdr_value:
            resistances.add("MDR")
        resistances = evaluate_mdr_mech(resistances)
        return "|".join(resistances)

    elif df.id_gruppo_microbo.iloc[0] == "psemal":
        sxt_value = _extract_value(df, "SXT")
        if pd.notnull(sxt_value) and sxt_value > 80:
            resistances.add("SXT")
        return "|".join(resistances)

    elif df.id_gruppo_microbo.iloc[0] == "staaur":
        oxa_value = _extract_value(df, "OXA")
        vancomicina_value = _extract_value(df, "VAN")
        if not pd.isnull(oxa_value) and oxa_value > 2:
            resistances.add("MRSA")
        if not pd.isnull(vancomicina_value) and vancomicina_value > 2:
            resistances.add("VANCO")
        return "|".join(resistances)

    elif df.id_gruppo_microbo.iloc[0] == "entspp":
        # esclude enterococcus gallinarum che è sempre resistente
        vancomicina_value = _extract_value(df, "VAN")
        df = df[~df.id_microbo.isin(["entgal", "entcas"])].copy()
        if not pd.isnull(vancomicina_value) and vancomicina_value > 4:
            resistances.add("VRE")
        return "|".join(resistances)
    elif df.id_gruppo_microbo.iloc[0] == "strpne":
        penicillina_value = _extract_value(df, "PEN")
        benzilpenicillina_value = _extract_value(df, "BPE")
        if (
            not pd.isnull(benzilpenicillina_value) and benzilpenicillina_value > 0.06
        ) or (not pd.isnull(penicillina_value) and penicillina_value > 0.06):
            resistances.add("PEN")
        return "|".join(resistances)
    # Se si arriva a questo punto si restituisce pd.NA
    return pd.NA


def check_resistance_and_validity(df, keep_cols=None):
    def _safe_iloc(serie, index):
        if len(serie):
            return serie.iloc[index]
        return pd.NA

    resistente = _check_resistance_and_validity(df.copy())
    if keep_cols is None:
        return df.assign(
            resistente=resistente,
        )
    return pd.Series(
        [_safe_iloc(df[c].mode(), 0) for c in keep_cols] + [resistente],
        index=[c for c in keep_cols] + ["resistente"],
    )


def get_resistance_or_not_instructions():
    microbo_mapper_reset_index = microbo_mapper.reset_index()
    microbo_id_list = microbo_mapper_reset_index.id_microbo.map(
        microbo_mapper.id_gruppo_microbo
    ).fillna(microbo_mapper_reset_index.id_microbo)
    fake_df = pd.DataFrame(
        [
            [
                0,
                microbo_id,
                "",
                "",
                pd.NA,
                pd.NA,
                pd.to_datetime("2023-01-01"),
            ]
            for microbo_id in microbo_id_list
        ],
        columns=[
            "id_richiesta",
            "id_gruppo_microbo",
            "id_microbo",
            "id_materiale",
            "id_antibiotico",
            "risultato_quantitativo",
            "data_prelievo",
        ],
    )
    values = (
        fake_df.groupby("id_gruppo_microbo")
        .apply(_check_resistance_and_validity)
        .notnull()
    )
    resistance_check = values.to_dict()

    return resistance_check
