from typing import List, Optional
from . import engine  # noqa
from arxivtrend.domain.repos import ArxivCacheRepoImpl
from arxivtrend.domain.entities import (
    ArxivQueryEntity, ArxivResultEntity,
    ArxivSummaryEntity
)
from arxivtrend.infra.mongo.models import (
    ArxivResult, ArxivSummary
)


class ArxivCacheRepo(ArxivCacheRepoImpl):

    def already_cached(
        self,
        q: ArxivQueryEntity
    ) -> bool:
        return ArxivResult.objects(
            search_q=q.search_q,
            category=q.category
        ).count() > 0

    def get_query(
        self,
        q: ArxivQueryEntity
    ) -> ArxivQueryEntity:
        result: ArxivResult = ArxivResult.objects(
            search_q=q.search_q,
            category=q.category
        ).first()

        if result is None:
            return None

        return ArxivQueryEntity(
            search_q=result.search_q,
            category=result.category,
            submitted_begin=result.submitted_begin,
            submitted_end=result.submitted_end
        )

    def get(
        self,
        q: ArxivQueryEntity
    ) -> Optional[ArxivResultEntity]:
        doc = ArxivResult.objects(
            search_q=q.search_q,
            category=q.category
        ).first()

        if doc is None:
            return None

        # doc.summaries.fetch()
        return doc.to_entity()

    def store(
        self,
        query: ArxivQueryEntity,
        results: List[ArxivSummaryEntity]
    ):
        doc: ArxivResult = ArxivResult.objects.filter(
            search_q=query.search_q,
            category=query.category
        ).first()

        if doc is not None:
            doc.update(push_all__results=results)
        else:
            summaries = [
                ArxivSummary.from_entity(r)
                for r in results
            ]

            doc = ArxivResult.from_query_entity(query)
            ArxivSummary.objects.insert(summaries)
            doc.summaries = summaries
            doc.save()

    def delete(
        self,
        query: ArxivQueryEntity,
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
