from pydantic import BaseModel, ConfigDict
from enum import StrEnum


class PosJpNotation(StrEnum):
    NOUN = "名詞"
    VERB = "動詞"
    ADJ = "形容詞"
    OTHER = "-"


class Token(BaseModel):
    word: str
    pos: PosJpNotation

    model_config = ConfigDict(frozen=True)
