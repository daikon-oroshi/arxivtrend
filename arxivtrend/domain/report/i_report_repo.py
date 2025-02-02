from abc import ABCMeta, abstractmethod
from arxivtrend.domain.entities import (
    ArxivQuery
)


class ReportRepoImpl(metaclass=ABCMeta):

    def __init__(self, query: ArxivQuery):
        self.query = query

    @abstractmethod
    def render_report(self):
        raise NotImplementedError()
