import unittest
import copy
from datetime import date
from arxivtrend.infra.report_repo import ReportRepo
from arxivtrend.domain.entities import ArxivQuery, Report


class TestReport(unittest.TestCase):

    def test_render(self):
        query = ArxivQuery(
            search_q="test",
            submitted_begin=date(year=2024, month=1, day=1),
            submitted_end=date(year=2025, month=1, day=1),
            category="math"
        )
        top20 = [
                    {
                        "token": {"word": "test1", "pos": "動詞"},
                        "count": 20
                    },
                    {
                        "token": {"word": "test2", "pos": "名詞"},
                        "count": 19
                    },
                    {
                        "token": {"word": "test3", "pos": "形容詞"},
                        "count": 18
                    },
                    {
                        "token": {"word": "test4", "pos": "動詞"},
                        "count": 17
                    },
                    {
                        "token": {"word": "test5", "pos": "動詞"},
                        "count": 16
                    },
                    {
                        "token": {"word": "test6", "pos": "動詞"},
                        "count": 15
                    },
                    {
                        "token": {"word": "test7", "pos": "動詞"},
                        "count": 14
                    },
                    {
                        "token": {"word": "test8", "pos": "動詞"},
                        "count": 13
                    },
                    {
                        "token": {"word": "test9", "pos": "動詞"},
                        "count": 12
                    },
                    {
                        "token": {"word": "test10", "pos": "動詞"},
                        "count": 11
                    },
                    {
                        "token": {"word": "test11", "pos": "動詞"},
                        "count": 10
                    }
                ]
        report = Report(**{
            "whole": {
                "top20": copy.deepcopy(top20),
                "noun": [],
                "verb": [],
                "adj": []
            },
            "annual": [
                {
                    "period_from": date(year=2022, month=1, day=1),
                    "token_counts": copy.deepcopy(top20)
                },
                {
                    "period_from": date(year=2023, month=1, day=1),
                    "token_counts": copy.deepcopy(top20)
                },
                {
                    "period_from": date(year=2024, month=1, day=1),
                    "token_counts": copy.deepcopy(top20)
                },
                {
                    "period_from": date(year=2025, month=1, day=1),
                    "token_counts": copy.deepcopy(top20)
                }
            ],
            "monthly": [

            ],
            "weekly": []
        })
        report_repo = ReportRepo(query=query, report=report)
        report_repo.render_report()
