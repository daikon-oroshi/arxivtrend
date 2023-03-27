from typing import List
from abc import ABCMeta, abstractmethod
import arxiv
from arxivtrend.domain.entities import (
    ArxivQueryEntity, ArxivResultEntity
)


class ArxivResultRepo(metaclass=ABCMeta):

    @abstractmethod
    def exists_same_query(
        self,
        q: ArxivQueryEntity
    ) -> bool:
        pass

    @abstractmethod
    def get(
        self,
        q: ArxivQueryEntity
    ) -> ArxivResultEntity:
        pass

    @abstractmethod
    def store(
        self,
        q: ArxivQueryEntity,
        results: List[arxiv.Result]
    ):
        pass
