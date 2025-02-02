from arxivtrend.infra.tokenizer import Tokenizer
from arxivtrend.infra.report_repo import ReportRepo
from arxivtrend.domain.entities import ArxivQuery


class ReportService():

    def __init__(self, query: ArxivQuery):
        self.report_repo = ReportRepo()
