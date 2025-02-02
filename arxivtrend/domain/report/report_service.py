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

    def __init__(self):
        self.date_interpolator = DateInterpolator()
        self.stop_words = self.get_stop_word()

    # TODO: mongo側でやりたい
    def aggregate(self, query: ArxivQuery) -> Report:
        cache_repo = ArxivCacheRepo()
        summaries = cache_repo.get_summaries(query)

        whole = self.whole_aggregate(summaries)

        years = self.date_interpolator.interpolate(
            query.submitted_begin,
            query.submitted_end,
            "year"
        )
        annual = self.period_aggregate(years, summaries, whole.top10)

        months = self.date_interpolator.interpolate(
            query.submitted_begin,
            query.submitted_end,
            "month"
        )
        monthly = [] if len(months) > LINEGRAPH_MAXLABELS \
            else self.period_aggregate(months, summaries, whole.top10)

        weeks = self.date_interpolator.interpolate(
            query.submitted_begin,
            query.submitted_end,
            "week"
        )
        weekly = [] if len(weeks) > LINEGRAPH_MAXLABELS \
            else self.period_aggregate(weeks, summaries, whole.top10)

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
    ) -> List[TokenCount]:
        ret = []
        for _b, _e in zip(period, period[1:]):
            token_counts = self._count_token(
                [
                    s for s in summaries
                    if _b <= s.published and s.published < _e
                ],
                token_list
            )
            ret.append(
                PeriodTokenCount(
                    period_from=_b,
                    token_counts=token_counts
                )
            )
        return ret

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
            top20=top20,
            noun=noun,
            verb=verb,
            adj=adj
        )

    def get_stop_word(self):
        # TODO: 外部から追加
        return Tokenizer.get_base_stopword()
