from arxivtrend.log import logger
from arxivtrend.domain.entities import (
    ArxivQueryEntity
)
from arxivtrend.domain.services import ArxivService
from arxivtrend.domain.repos import (
    ArxivCacheRepoImpl
)
from arxivtrend.infra.mongo.arxiv_cache import (
    ArxivCacheRepo
)


class SearchUsecase():
    arxiv_service = ArxivService()
    cache_repo: ArxivCacheRepoImpl = ArxivCacheRepo()

    def search_and_cache_arxiv(
        self,
        query: ArxivQueryEntity,
        force_reacquire: bool
    ):
        cached_q = self.cache_repo.get_cached_query(query)
        if cached_q is None:
            # acquisition
            self.arxiv_service.search_and_cache(query)
            return

        elif cached_q.submitted_begin == query.submitted_begin \
                and cached_q.submitted_end == query.submitted_end:
            # skip
            logger.info("The arxiv data is cached, so the search is omitted.")
        else:
            if force_reacquire:
                self.delete_cache(query)
                self.arxiv_service.search_and_cache(query)
                return
            else:
                msg = f"The specified submitted span is " \
                    f"{query.submitted_begin} ~ {query.submitted_end}\n" \
                    f"but the cached submitted span is " \
                    f"{cached_q.submitted_begin} ~ " \
                    f"{cached_q.submitted_end}.\n" \
                    "Do you want to reacquire? y or n ? >> "
                yn = input(msg)

                if yn in ['y', 'Y', 'yes', 'Yes', 'YES']:
                    self.delete_cache(query)
                    self.arxiv_service.search_and_cache(query)
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
