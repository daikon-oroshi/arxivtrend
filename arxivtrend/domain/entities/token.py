from pydantic import BaseModel
from enum import StrEnum


class PosJpNotation(StrEnum):
    NOUN = "名詞"
    VERB = "動詞"
    ADJ = "形容詞"
    OHTER = "--"


class Token(BaseModel):
    word: str
    pos: PosJpNotation
