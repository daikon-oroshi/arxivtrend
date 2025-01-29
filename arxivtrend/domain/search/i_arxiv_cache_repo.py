from typing import List
from abc import ABCMeta, abstractmethod
import arxiv
from arxivtrend.domain.search.entities import (
    ArxivQuery, ArxivResultEntity
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
    ) -> ArxivResultEntity:
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
