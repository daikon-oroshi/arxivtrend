from arxivtrend.log import logger
from arxivtrend.domain.entities import (
    ArxivQueryEntity
)
from arxivtrend.domain.search import (
    SearchService, ArxivCacheRepoImpl,
    CacheState
)
from arxivtrend.infra.mongo.arxiv_cache_repo import (
    ArxivCacheRepo
)


class SearchUsecase():

    def __init__(self):
        self.search_service = SearchService()
        self.cache_repo: ArxivCacheRepoImpl = ArxivCacheRepo()

    def search_and_cache_arxiv(
        self,
        query: ArxivQueryEntity,
        force_reacquire: bool
    ):
        cached_state = self.search_service.get_cache_state(query)
        if cached_state == CacheState.NO:
            # acquisition
            self.search_service.search_and_cache(query)
            return

        elif cached_state == CacheState.ALL:
            # skip
            logger.info("The arxiv data is cached, so the search is omitted.")
            return

        if force_reacquire:
            self.delete_cache(query)
            self.search_service.search_and_cache(query)
            return
        else:
            cached_q = self.cache_repo.get_cached_query(query)
            msg = f"The specified submitted span is " \
                f"{query.submitted_begin} ~ {query.submitted_end}\n" \
                f"but the cached submitted span is " \
                f"{cached_q.submitted_begin} ~ " \
                f"{cached_q.submitted_end}.\n" \
                "Do you want to reacquire? y or n ? >> "
            yn = input(msg)

            if yn.lower() in ['y', 'yes']:
                self.delete_cache(query)
                self.search_service.search_and_cache(query)
            else:
                logger.info("Do not reacquire.")
                return

    def delete_cache(
        self,
        query: ArxivQueryEntity
    ):
        self.cache_repo.delete(query)

    def delete_cache_all(self):
        self.cache_repo.delete_all()
