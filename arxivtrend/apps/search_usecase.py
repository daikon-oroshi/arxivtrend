import json
from arxivtrend.log import logger
from arxivtrend.domain.entities import (
    ArxivQuery
)
from arxivtrend.domain.search \
    import CacheState, SearchService
from arxivtrend.infra.mongo \
    import ArxivCacheRepo
from arxivtrend.infra.arxiv_api import ArxivSearch
from arxivtrend.infra.mongo.engine import Connection
from arxivtrend.infra.report_repo import ReportRepo
from arxivtrend.domain.report import ReportService


class SearchUsecase():

    def __init__(self):
        self.search_service = SearchService()
        self.arvix_search = ArxivSearch()
        self.cache_repo = ArxivCacheRepo()

    def create(
        self,
        query: ArxivQuery,
        force_reacquire: bool,
        stop_query_word: bool = False
    ):
        with Connection():
            self.__search_and_cache(query, force_reacquire)
            report_service = ReportService(
                query=query,
                stop_query_word=stop_query_word
            )
            report = report_service.aggregate(query)

            report_repo = ReportRepo(query)
            report_repo.render_report(report)

    def __search_and_cache(
        self,
        query: ArxivQuery,
        force_reacquire: bool
    ):
        cached_state = self.search_service.get_cache_state(query)
        if cached_state == CacheState.NO:
            # acquisition
            self.search_service.search_and_cache(query)
            return

        elif cached_state == CacheState.ALL:
            # skip
            msg = "The arxiv data is cached, so the search is omitted."
            logger.info(msg)
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
                f"The missing period is treated as if there is no paper.\n" \
                "Do you want to reacquire (再取得)? y or n ? >> "
            yn = input(msg)

            if yn.lower() in ['y', 'yes']:
                self.delete_cache(query)
                self.search_service.search_and_cache(query)
            else:
                logger.info("Do not reacquire.")
                return

    def delete_cache(
        self,
        query: ArxivQuery
    ):
        with Connection():
            self.cache_repo.delete(query)

    def delete_cache_all(self):
        with Connection():
            self.cache_repo.delete_all()

    def show_categories(self) -> dict:
        categories = self.arvix_search.get_categories()
        print(json.dumps(categories, indent=2))

    def show_query_str(self, query: ArxivQuery):
        # 件数確認用にqueryを取得
        # https://export.arxiv.org/api/query?search_query={query_str}
        # で確認できる
        # TODO: count にする
        query_str = self.arvix_search._make_query_str(query)
        print(query_str)
