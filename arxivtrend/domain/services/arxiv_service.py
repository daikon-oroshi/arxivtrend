from typing import Generator, Optional, List
from arxivtrend.log import logger
from arxivtrend.domain.entities import (
    ArxivQueryEntity, ArxivSummaryEntity,
)
from arxivtrend.domain.repos import ArxivSearchRepo


class ArxivApi():

    def search(
        self,
        q: ArxivQueryEntity,
        max_results: Optional[int] = float('inf')
    ) -> Generator[ArxivSummaryEntity, None, None]:
        q_str = self.make_query_str(q)
        logger.debug(q_str)

        for r in ArxivSearchRepo.search():
            yield r

    def store(
        self,
        q: ArxivQueryEntity,
        results: List[ArxivSummaryEntity]
    ) -> None:
        pass
