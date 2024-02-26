from dataclasses import dataclass
from typing import Callable, List, Union


@dataclass
class _instruction:
    tag: str
    descrizione: str
    gruppo_microbo_id: str
    descrizione_gruppo_microbo: str
    cutoff_repeat_days: int = None


@dataclass
class _rate_instruction:
    tag: str
    descrizione: str
    id_gruppo_microbi: Union[str, List[str]]
    descrizione_gruppo_microbi: str
    select_fn: Callable
    cutoff_repeat_days: int = None


def autogenerate(df, tag: str, tag_description: str):
    return [
        _instruction(
            tag,
            tag_description,
            row.id_gruppo_microbo,
            row.nome_gruppo_microbo,
        )
        for _, row in (
            df[["id_gruppo_microbo", "nome_gruppo_microbo"]]
            .drop_duplicates()
            .reset_index(drop=True)
        ).iterrows()
    ]
