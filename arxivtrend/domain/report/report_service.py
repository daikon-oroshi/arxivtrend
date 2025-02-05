from typing import List
from collections import defaultdict
from datetime import date

from arxivtrend.infra.tokenizer import Tokenizer
from arxivtrend.infra.mongo.arxiv_cache_repo import ArxivCacheRepo
from arxivtrend.domain.entities import (
    ArxivQuery, ArxivSummaryEntity,
    Report, WholePeriodData,
    TokenCount, Token,
    PosJpNotation, PeriodTokenCount,
    LINEGRAPH_MAXLABELS
)
from .date_interpolator import DateInterpolator


class ReportService():

    def __init__(
        self,
        query: ArxivQuery,
        stop_query_word: bool = False
    ):
        self.date_interpolator = DateInterpolator()
        self.stop_words = Tokenizer.get_stopword()
        if stop_query_word:
            self.stop_words.extend(query.search_q.split())

    # TODO: mongo側でやりたい
    def aggregate(self, query: ArxivQuery) -> Report:
        cache_repo = ArxivCacheRepo()
        summaries = cache_repo.get_summaries(query)

        whole = self.whole_aggregate(summaries)
        top10_tokens = [
            tc.token for tc in whole.top10
        ]

        years = self.date_interpolator.interpolate(
            query.submitted_begin,
            query.submitted_end,
            "year"
        )
        annual = self.period_aggregate(years, summaries, top10_tokens)

        months = self.date_interpolator.interpolate(
            query.submitted_begin,
            query.submitted_end,
            "month"
        )
        monthly = [] if len(months) > LINEGRAPH_MAXLABELS \
            else self.period_aggregate(months, summaries, top10_tokens)

        weeks = self.date_interpolator.interpolate(
            query.submitted_begin,
            query.submitted_end,
            "week"
        )
        weekly = [] if len(weeks) > LINEGRAPH_MAXLABELS \
            else self.period_aggregate(weeks, summaries, top10_tokens)

        return Report(
            whole=whole,
            annual=annual,
            monthly=monthly,
            weekly=weekly
        )

    def period_aggregate(
        self,
        period: List[date],
        summaries: List[ArxivSummaryEntity],
        token_list: List[Token] | None = None
    ) -> List[PeriodTokenCount]:
        period_token_counts = []
        for _b, _e in zip(period, period[1:]):
            period_summ = [
                s for s in summaries
                if _b <= s.published and s.published < _e
            ]
            token_counts = self._count_token(
                period_summ,
                token_list
            )
            period_token_counts.append(
                PeriodTokenCount(
                    period_from=_b,
                    paper_count=len(period_summ),
                    token_counts=token_counts
                )
            )
        return period_token_counts

    def _count_token(
        self,
        summaries: List[ArxivSummaryEntity],
        token_list: List[Token] | None = None
    ) -> List[TokenCount]:

        token_counter = defaultdict(lambda: 0)  # initialize 0
        for s in summaries:
            for t in s.tokens:
                if t.word in self.stop_words:
                    continue
                if t.pos == PosJpNotation.OTHER:
                    continue
                if token_list is not None and t not in token_list:
                    continue
                token_counter[t] += 1

        return [
            TokenCount(token=token, count=count)
            for (token, count)
            in sorted(
                token_counter.items(),
                key=lambda x: x[1],
                reverse=True
            )
        ]

    def whole_aggregate(
        self,
        summaries: List[ArxivSummaryEntity],
    ) -> WholePeriodData:
        whole_count = self._count_token(summaries)
        top20 = whole_count[0:20]
        noun = [
            tc for tc in whole_count
            if tc.token.pos == PosJpNotation.NOUN
        ][0:20]
        verb = [
            tc for tc in whole_count
            if tc.token.pos == PosJpNotation.VERB
        ][0:20]
        adj = [
            tc for tc in whole_count
            if tc.token.pos == PosJpNotation.ADJ
        ][0:20]
        return WholePeriodData(
            paper_count=len(summaries),
            top20=top20,
            noun=noun,
            verb=verb,
            adj=adj
        )
