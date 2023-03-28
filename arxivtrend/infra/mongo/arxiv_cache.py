from typing import List, Optional
from . import engine  # noqa
from arxivtrend.domain.repos import ArxivCacheRepoImpl
from arxivtrend.domain.entities import (
    ArxivQueryEntity, ArxivResultEntity,
    ArxivSummaryEntity
)
from arxivtrend.infra.mongo.models import (
    ArxivResult
)


class ArxivCacheRepo(ArxivCacheRepoImpl):

    def exists_same_query(
        self,
        q: ArxivQueryEntity
    ) -> bool:
        return ArxivResult.objects.count(
            search_q=q.search_q,
            category=q.category
        ) > 0

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

        doc.results.fetch()
        return doc.to_entity()

    def store(
        self,
        query: ArxivQueryEntity,
        results: List[ArxivSummaryEntity]
    ):
        doc: ArxivResult = ArxivResult.objects(
            search_q=query.search_q,
            category=query.category
        ).first()

        if doc is not None:
            doc.update(push_all__results=results)
        else:
            doc = ArxivResult.from_entity(
                ArxivResultEntity(
                    query=query,
                    results=results
                )
            )
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
            doc.delete()
