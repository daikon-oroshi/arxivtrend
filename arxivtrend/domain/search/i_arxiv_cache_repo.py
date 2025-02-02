from typing import List
from abc import ABCMeta, abstractmethod
import arxiv
from arxivtrend.domain.entities import (
    ArxivQuery, ArxivSummaryEntity
)


class ArxivCacheRepoImpl(metaclass=ABCMeta):

    @abstractmethod
    def get_cached_query(
        self,
        q: ArxivQuery
    ) -> ArxivQuery:
        raise NotImplementedError()

    @abstractmethod
    def get(
        self,
        q: ArxivQuery
    ) -> List[ArxivSummaryEntity]:
        raise NotImplementedError()

    @abstractmethod
    def store(
        self,
        q: ArxivQuery,
        results: List[arxiv.Result]
    ):
        raise NotImplementedError()

    @abstractmethod
    def delete(
        self,
        q: ArxivQuery,
    ):
        raise NotImplementedError()

    @abstractmethod
    def delete_all(
        self
    ):
        raise NotImplementedError()
