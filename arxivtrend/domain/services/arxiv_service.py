from typing import Generator, Optional, List
import arxiv
from arxivtrend.log import logger
from arxivtrend.domain.entities import ArxivQueryEntity


class ArxivApi():

    def search(
        self,
        q: ArxivQueryEntity,
        max_results: Optional[int] = float('inf')
    ) -> Generator[arxiv.Result, None, None]:
        q_str = self.make_query_str(q)
        logger.debug(q_str)

        search = arxiv.Search(
            query=q_str,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            max_results=max_results
        )
        for r in search.results():
            yield r

    def store(
        self,
        q: ArxivQueryEntity,
        results: List[arxiv.Result]
    ) -> None:
        pass
