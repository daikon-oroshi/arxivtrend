from typing import Generator
from abc import ABCMeta, abstractmethod
from arxivtrend.domain.entities import (
    ArxivQuery, ArxivSummaryEntity
)


class ArxivSearchImpl(metaclass=ABCMeta):

    @abstractmethod
    def get_categories(self) -> dict:
        raise NotImplementedError()

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
