from arxivtrend.log import logger
from arxivtrend.domain.entities import (
    ArxivQueryEntity
)
from arxivtrend.domain.repos \
    import ArxivSearchImpl, ArxivCacheRepoImpl
from arxivtrend.infra.arxiv_api.arxiv_search \
      import ArxivSearch
from arxivtrend.infra.mongo.arxiv_cache import ArxivCacheRepo


class ArxivService():

    BUFF_SIZE = 500

    search_repo: ArxivSearchImpl = ArxivSearch()
    cache_repo: ArxivCacheRepoImpl = ArxivCacheRepo()

    def __log_of_count_of_papers(self, count: int):
        print(f"\r Count of papers: {count}\n", end="")

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
                self.__log_of_count_of_papers(count)

        else:
            if len(buffer) > 0:
                self.cache_repo.store(
                    q,
                    buffer
                )
        self.__log_of_count_of_papers(count)
        logger.info(f"get {count} papers")
