from typing import List
from datetime import date
from pydantic import BaseModel
from .arxiv_query import ArxivQueryEntity
import arxiv


class ArxivSummaryEntity(BaseModel):
    entry_id: str
    updated: date
    published: date
    title: str
    authors: List[str]
    summary: str
    categories: List[str]

    @classmethod
    def from_arxiv_result(
        cls,
        result: arxiv.Result
    ) -> "ArxivSummaryEntity":
        return ArxivSummaryEntity(
            entry_id=result.entry_id,
            updated=result.updated,
            published=result.published,
            title=result.title,
            authors=[a.name for a in result.authors],
            summary=result.summary,
            categories=result.categories
        )


class ArxivResultEntity(BaseModel):
    query: ArxivQueryEntity
    results: List[ArxivSummaryEntity]
