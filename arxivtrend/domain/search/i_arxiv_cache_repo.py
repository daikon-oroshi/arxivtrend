from typing import List
from abc import ABCMeta, abstractmethod
import arxiv
from arxivtrend.domain.entities import (
    ArxivQueryEntity, ArxivResultEntity
)


class ArxivCacheRepoImpl(metaclass=ABCMeta):

    @abstractmethod
    def get_cached_query(
        self,
        q: ArxivQueryEntity
    ) -> ArxivQueryEntity:
        raise NotImplementedError()

    @abstractmethod
    def get(
        self,
        q: ArxivQueryEntity
    ) -> ArxivResultEntity:
        raise NotImplementedError()

    @abstractmethod
    def store(
        self,
        q: ArxivQueryEntity,
        results: List[arxiv.Result]
    ):
        raise NotImplementedError()

    @abstractmethod
    def delete(
        self,
        q: ArxivQueryEntity,
    ):
        raise NotImplementedError()

    @abstractmethod
    def delete_all(
        self
    ):
        raise NotImplementedError()
