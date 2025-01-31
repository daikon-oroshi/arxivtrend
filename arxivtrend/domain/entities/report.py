from typing import List
from enum import StrEnum
from pydantic import BaseModel, Field, field_validator
from datetime import date


class PosJpNotation(StrEnum):
    NOUN = "名詞"
    VERB = "動詞"
    ADJ = "形容詞"


class Token(BaseModel):
    word: str
    pos: PosJpNotation


class TokenCount(BaseModel):
    token: Token
    count: int


class PeriodTokenCount(BaseModel):
    period_from: date
    token_counts: List[TokenCount] = Field(..., max_length=20)

    @property
    def max_of_count(self) -> int:
        return max([
            tc.count for tc in self.token_counts
        ])

    def get_count_by_word(
        self,
        token: Token
    ) -> int:
        for tc in self.token_counts:
            if tc.token == token:
                return tc.count
        return 0


class WholePeriodData(BaseModel):
    top20: List[TokenCount] = Field(..., max_length=20)
    noun: List[TokenCount] = Field(..., max_length=20)
    verb: List[TokenCount] = Field(..., max_length=20)
    adj: List[TokenCount] = Field(..., max_length=20)

    @field_validator("top20")
    @classmethod
    def sort_top20(cls, top20: List[TokenCount]):
        # countでsort
        # validatorでやることではないかも
        top20.sort(key=lambda w: w.count, reverse=True)
        return top20

    @field_validator("noun")
    @classmethod
    def sort_noun(cls, noun: List[TokenCount]):
        noun.sort(key=lambda w: w.count, reverse=True)
        return noun

    @field_validator("verb")
    @classmethod
    def srot_verb(cls, verb: List[TokenCount]):
        verb.sort(key=lambda w: w.count, reverse=True)
        return verb

    @field_validator("adj")
    @classmethod
    def validate_adj(cls, adj: List[TokenCount]):
        adj.sort(key=lambda w: w.count, reverse=True)
        return adj

    @property
    def top10(self) -> List[TokenCount]:
        return self.top20[0:10]

    @property
    def max_of_count(self) -> int:
        return max([
            w.count for w in self.top20
        ])

    @property
    def top10_tokens(self) -> List[Token]:
        return [
            tc.token
            for tc in self.top10
        ]


class Report(BaseModel):
    whole: WholePeriodData
    annual: List[PeriodTokenCount] = Field(..., max_length=100)
    monthly: List[PeriodTokenCount] = Field(..., max_length=100)
    weekly: List[PeriodTokenCount] = Field(..., max_length=100)

    @field_validator("annual")
    @classmethod
    def srot_annual(cls, annual: List[PeriodTokenCount]):
        annual.sort(key=lambda w: w.period_from)
        return annual

    @field_validator("monthly")
    @classmethod
    def srot_monthly(cls, monthly: List[PeriodTokenCount]):
        monthly.sort(key=lambda w: w.period_from)
        return monthly

    @field_validator("weekly")
    @classmethod
    def sort_weekly(cls, weekly: List[PeriodTokenCount]):
        weekly.sort(key=lambda w: w.period_from)
        return weekly

    @property
    def annual_max_of_count(self):
        return max([
            a.max_of_count for a in self.annual
        ])

    @property
    def monthly_max_of_count(self):
        return max([
            m.max_of_count for m in self.monthly
        ])

    @property
    def weekly_max_of_count(self):
        return max([
            w.max_of_count for w in self.weekly
        ])
