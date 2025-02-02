from typing import List
from arxivtrend.domain.entities import (
    ArxivQuery,
    ArxivSummaryEntity
)
from arxivtrend.infra.mongo import (
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
    ) -> List[ArxivSummary]:
        doc = ArxivResult.objects(
            search_q=q.search_q,
            category=q.category
        ).first()

        if doc is None:
            return []

        summaries = ArxivSummary.objects().filter(
            pk__in=[s.pk for s in doc.summaries],
            published__gte=q.submitted_begin,
            published__lte=q.submitted_end,
        )

        return [
            s.to_entity() for s in summaries
        ]

    def store(
        self,
        query: ArxivQuery,
        results: List[ArxivSummaryEntity]
    ):
        summaries = [
            ArxivSummary.from_entity(r)
            for r in results
        ]
        ArxivSummary.objects.insert(summaries)

        doc: ArxivResult = ArxivResult.objects.filter(
            search_q=query.search_q,
            category=query.category
        ).first()

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
