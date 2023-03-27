from typing import List, Optional, Generator
import arxiv

from arxivtrend.domain.repos import ArxivTaxonomyRepo
from .taxonomies import taxonomies
from arxivtrend.domain.entities import (
    ArxivQueryEntity, ArxivSummaryEntity
)


class ArxivSearch(ArxivTaxonomyRepo):
    @staticmethod
    def get_partial_match_taxonomies(cat_q: str) -> List[str]:
        if cat_q is None or cat_q == "":
            return []

        ret = []
        for taxos in taxonomies.values():
            ret.extend([
                t for t in taxos
                if cat_q in t
            ])
        return ret

    def search(
        self,
        q: ArxivQueryEntity,
        max_results: Optional[int] = float('inf')
    ) -> Generator[ArxivSummaryEntity, None, None]:

        search = arxiv.Search(
            query=self.make_query_str(q),
            sort_by=arxiv.SortCriterion.SubmittedDate,
            max_results=max_results
        )

        for r in search.result():
            yield ArxivSummaryEntity.from_arxiv_result(r)

    def make_query_str(
        self,
        query: ArxivQueryEntity
    ) -> str:
        q = []
        q.append(
            f"ti:\"{query.search_q}\""
        )

        taxos = ArxivTaxonomyRepo. \
            get_partial_match_taxonomies(query.category)

        if taxos:
            sep = " OR "
            category = sep.join([
                f"cat:\"{t}\"" for t in taxos
            ])
            q.append(f"({category})")

        duration = "submittedDate: " \
            f"[{query.submitted_begin.strftime('%Y%m%d')}" \
            f" TO {query.submitted_end.strftime('%Y%m%d')}]"

        q.append(duration)

        return " AND ".join(q)
