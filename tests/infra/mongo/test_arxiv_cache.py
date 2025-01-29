import unittest
import datetime
from arxivtrend.infra.mongo.arxiv_cache_repo import ArxivCacheRepo

from arxivtrend.infra.mongo.models import (
    ArxivResult, ArxivSummary
)
from arxivtrend.domain.search.entities import (
    ArxivQuery, ArxivSummaryEntity,
    ArxivResultEntity
)


def is_db_initial_state():
    return ArxivResult.objects.count() == 0


@unittest.skipIf(
    not is_db_initial_state(),
    "Initialize mongo db before run these tests."
)
class TestArxivCacheRepo(unittest.TestCase):

    TEST_QUERY_ENTITY = ArxivQuery(
        search_q="test",
        category="test"
    )

    TEST_ARXIV_SUMMARY_ENTITIES = [
        ArxivSummaryEntity(
            entry_id=1,
            updated=datetime.date.today(),
            published=datetime.date.today(),
            title="test",
            authors=["test"],
            summary="test",
            categories=["test"]
        )
    ]

    def tearDown(self):
        repo = ArxivCacheRepo()
        repo.delete(self.TEST_QUERY_ENTITY)

    def test_store(self):
        repo = ArxivCacheRepo()

        self.assertEqual(
            ArxivResult.objects.count(),
            0
        )
        self.assertEqual(
            ArxivSummary.objects.count(),
            0
        )

        repo.store(
            self.TEST_QUERY_ENTITY,
            self.TEST_ARXIV_SUMMARY_ENTITIES
        )
        self.assertEqual(
            ArxivResult.objects.count(),
            1
        )
        self.assertEqual(
            ArxivSummary.objects.count(),
            1
        )

        repo.store(
            self.TEST_QUERY_ENTITY,
            self.TEST_ARXIV_SUMMARY_ENTITIES
        )
        self.assertEqual(
            ArxivResult.objects.count(),
            1
        )
        self.assertEqual(
            ArxivSummary.objects.count(),
            2
        )

    def test_get(self):
        repo = ArxivCacheRepo()
        repo.store(
            self.TEST_QUERY_ENTITY,
            self.TEST_ARXIV_SUMMARY_ENTITIES
        )

        query = repo.get_cached_query(
            self.TEST_QUERY_ENTITY
        )

        result = repo.get(
            self.TEST_QUERY_ENTITY
        )

        self.assertEqual(
            query, self.TEST_QUERY_ENTITY
        )
        self.assertEqual(
            result,
            ArxivResultEntity(
                query=self.TEST_QUERY_ENTITY,
                results=self.TEST_ARXIV_SUMMARY_ENTITIES
            )
        )

    def test_delete(self):
        repo = ArxivCacheRepo()

        repo.delete(self.TEST_QUERY_ENTITY)
        self.assertEqual(
            repo.get_cached_query(
                self.TEST_QUERY_ENTITY
            ),
            None
        )


if __name__ == "__main__":
    unittest.main()
