from arxivtrend.lib.word_extract import WordExtractor
from arxivtrend.infra.repo import ReportRepo
from arxivtrend.domain.entities import ArxivQuery


class ReportService():

    def __init__(self, query: ArxivQuery):
        self.word_extractor: WordExtractor = WordExtractor()

        self.report_repo = ReportRepo()
