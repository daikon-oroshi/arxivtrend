from arxivtrend.log import logger
from arxivtrend.domain.entities import (
    ArxivQueryEntity
)
from arxivtrend.domain.search import (
    ArxivSearchImpl, ArxivCacheRepoImpl,
    CacheState
)
from arxivtrend.infra.arxiv_api.arxiv_search \
      import ArxivSearch
from arxivtrend.infra.mongo.arxiv_cache_repo import ArxivCacheRepo


class SearchService():

    BUFF_SIZE = 500

    search_repo: ArxivSearchImpl = ArxivSearch()
    cache_repo: ArxivCacheRepoImpl = ArxivCacheRepo()

    def __log_count_of_papers(self, count: int):
        print(f"\r Count of papers: {count}\n", end="")

    def get_cache_state(
        self,
        query: ArxivQueryEntity
    ) -> CacheState:
        cached_q = self.cache_repo.get_cached_query(query)
        if cached_q is None:
            return CacheState.NO
        if cached_q.submitted_begin == query.submitted_begin \
                and cached_q.submitted_end == query.submitted_end:
            return CacheState.ALL
        else:
            CacheState.PARTLY

    def search_and_cache(
        self,
        q: ArxivQueryEntity
    ):
        buffer = []
        count = 0
        for r in self.search_repo.search(q):
            buffer.append(r)
            count = count + 1

            if len(buffer) >= self.BUFF_SIZE:
                self.cache_repo.store(
                    q,
                    buffer
                )
                buffer = []
                self.__log_count_of_papers(count)

        else:
            if len(buffer) > 0:
                self.cache_repo.store(
                    q,
                    buffer
                )
        self.__log_count_of_papers(count)
        logger.info(f"get {count} papers")
