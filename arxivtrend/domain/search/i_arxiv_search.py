from typing import Generator
from abc import ABCMeta, abstractmethod
from arxivtrend.domain.entities import (
    ArxivQuery, ArxivSummaryEntity
)
from arxivtrend.infra.arxiv_api import ArxivSearch


class ArxivSearchImpl(metaclass=ABCMeta):

    def __init__(self):
        self.arxiv_search = ArxivSearch()

    @abstractmethod
    def search(
        self,
        q: ArxivQuery,
        max_results: int | None = None
    ) -> Generator[ArxivSummaryEntity, None, None]:
        raise NotImplementedError()

    @abstractmethod
    def count(
        self,
        q: ArxivQuery
    ) -> int:
        raise NotImplementedError()
