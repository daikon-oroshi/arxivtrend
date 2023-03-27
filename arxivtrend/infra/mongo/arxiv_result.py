from typing import List
import arxiv
from . import engine  # noqa
from arxivtrend.domain.repos import ArxivResultRepo
from arxivtrend.domain.entities import (
    ArxivQueryEntity, ArxivResultEntity
)


class ArxivResult(ArxivResultRepo):

    def exists_same_query(
        self,
        q: ArxivQueryEntity
    ) -> bool:
        pass

    def get(
        self,
        q: ArxivQueryEntity
    ) -> ArxivResultEntity:
        pass

    def store(
        self,
        q: ArxivQueryEntity,
        results: List[arxiv.Result]
    ):
        pass
