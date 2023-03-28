from typing import List, Optional, Generator
from abc import ABCMeta, abstractmethod
from arxivtrend.domain.entities import (
    ArxivQueryEntity, ArxivSummaryEntity
)


class ArxivSearchRepoImpl(metaclass=ABCMeta):

    @abstractmethod
    @staticmethod
    def get_partial_match_taxonomies(
        self,
        category_q: str
    ) -> List[str]:
        pass

    @abstractmethod
    def search(
        self,
        q: ArxivQueryEntity,
        max_results: Optional[int] = float('inf')
    ) -> Generator[ArxivSummaryEntity, None, None]:
        pass
