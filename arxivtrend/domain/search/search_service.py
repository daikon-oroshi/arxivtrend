from arxivtrend.log import logger
from arxivtrend.domain.entities import ArxivQuery
from arxivtrend.infra.arxiv_api \
    import ArxivSearch
from arxivtrend.infra.mongo \
    import ArxivCacheRepo
from .cache_status import CacheState
from arxivtrend.infra.tokenizer import Tokenizer


class SearchService():

    BUFF_SIZE = 500

    def __init__(self):
        self.search_repo = ArxivSearch()
        self.word_extractor = Tokenizer()
        self.cache_repo = ArxivCacheRepo()

    def __log_count_of_papers(self, count: int):
        print(f"\r Count of papers: {count}\n", end="")

    def get_cache_state(
        self,
        query: ArxivQuery
    ) -> CacheState:
        cached_q = self.cache_repo.get_cached_query(query)
        if cached_q is None:
            return CacheState.NO
        if cached_q.submitted_begin <= query.submitted_begin \
                and query.submitted_end <= cached_q.submitted_end:
            return CacheState.ALL
        else:
            CacheState.PARTLY

    def search_and_cache(
        self,
        q: ArxivQuery
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
