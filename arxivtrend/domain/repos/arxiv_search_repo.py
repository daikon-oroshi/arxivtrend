from typing import List, Optional, Generator
from abc import ABCMeta, abstractmethod
from arxivtrend.domain.entities import (
    ArxivQueryEntity, ArxivSummaryEntity
)


class ArxivSearchImpl(metaclass=ABCMeta):

    @staticmethod
    def get_partial_match_taxonomies(
        category_q: str
    ) -> List[str]:
        raise NotImplementedError()

    @abstractmethod
    def search(
        self,
        q: ArxivQueryEntity,
        max_results: Optional[int] = float('inf')
    ) -> Generator[ArxivSummaryEntity, None, None]:
        raise NotImplementedError()

    @abstractmethod
    def count(
        self,
        q: ArxivQueryEntity
    ) -> int:
        raise NotImplementedError()
