from typing import List, Optional
from . import engine  # noqa
from arxivtrend.domain.search import (
    ArxivQuery, ArxivResultEntity,
    ArxivSummaryEntity
)
from arxivtrend.infra.mongo.models import (
    ArxivResult, ArxivSummary
)


class ArxivCacheRepo():

    def get_cached_query(
        self,
        q: ArxivQuery
    ) -> ArxivQuery:
        result: ArxivResult = ArxivResult.objects(
            search_q=q.search_q,
            category=q.category
        ).first()

        if result is None:
            return None

        return ArxivQuery(
            search_q=result.search_q,
            category=result.category,
            submitted_begin=result.submitted_begin,
            submitted_end=result.submitted_end
        )

    def get(
        self,
        q: ArxivQuery
    ) -> Optional[ArxivResultEntity]:
        doc = ArxivResult.objects(
            search_q=q.search_q,
            category=q.category
        ).first()

        if doc is None:
            return None

        return doc.to_entity()

    def store(
        self,
        query: ArxivQuery,
        results: List[ArxivSummaryEntity]
    ):

        doc: ArxivResult = ArxivResult.objects.filter(
            search_q=query.search_q,
            category=query.category
        ).first()

        summaries = [
            ArxivSummary.from_entity(r)
            for r in results
        ]
        ArxivSummary.objects.insert(summaries)

        if doc is not None:
            doc.update(push_all__summaries=summaries)
        else:
            doc = ArxivResult.from_query_entity(query)
            doc.summaries = summaries
            doc.save()

    def delete(
        self,
        query: ArxivQuery,
    ):
        doc: ArxivResult = ArxivResult.objects(
            search_q=query.search_q,
            category=query.category
        ).first()

        if doc is not None:
            ArxivSummary.objects().filter(pk__in=[
                s.pk for s in doc.summaries
            ]).delete()
            doc.delete()

    def delete_all(
        self
    ):
        ArxivSummary.objects().delete()
        ArxivResult.objects().delete()
