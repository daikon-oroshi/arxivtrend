from typing import Generator, Optional, Dict
from datetime import date
from pydantic import BaseModel, validator
import arxiv
from arxivtrend.arxiv_api.taxonomy import get_partial_match_taxonomies
from arxivtrend.log import logger


class Query(BaseModel):
    search_q: str
    submitted_begin: Optional[date]
    submitted_end: Optional[date]
    category: Optional[str]

    @validator("submitted_begin")
    def default_submitted_begin(cls, v: Optional[date]) -> date:
        if v is None:
            # Beginning of the year when the arxiv service was launched
            v = date(1991, 1, 1)
        return v

    @validator("submitted_end")
    def span_is_valid(cls, v: Optional[date], values: Dict) -> date:
        # default value
        if v is None:
            v = date.today()
        if v < values["submitted_begin"]:
            raise ValueError(
                "submitted_begin must"
                + "be earlier than submitted_end."
            )
        return v


class ArxivApi():

    def search(
        self,
        q: Query,
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

    def make_query_str(
        self,
        query: Query
    ) -> str:
        q = []
        q.append(
            f"ti:\"{query.search_q}\""
        )

        taxos = []
        if query.category is not None or query.category != "":
            taxos = get_partial_match_taxonomies(query.category)

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
