from typing import List
from abc import ABCMeta, abstractmethod


class ArxivTaxonomyRepo(metaclass=ABCMeta):

    @abstractmethod
    def get_partial_match_taxonomies(
        self,
        category_q: str
    ) -> List[str]:
        pass
