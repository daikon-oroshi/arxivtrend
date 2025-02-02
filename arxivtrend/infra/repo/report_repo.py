from arxivtrend.env import env
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from arxivtrend.domain.entities import Report, ArxivQuery
from arxivtrend.domain.report.i_report_repo import ReportRepoImpl


class ReportRepo(ReportRepoImpl):

    def __init__(self, query: ArxivQuery):
        self.query = query

    def _save_dir(self) -> Path:
        _dir_name = f"{self.query.search_q}_" \
            f"{self.query.submitted_begin}_" \
            f"{self.query.submitted_end}_" \
            f"{self.query.category}"

        return Path(env.REPORT_SAVE_DIR, _dir_name)

    def _save(self, adoc: str):
        save_dir = self._save_dir()
        save_dir.mkdir(parents=True, exist_ok=True)

        save_path = save_dir.joinpath("report.adoc")

        with save_path.open(mode='w') as f:
            f.write(adoc)

    def render_report(self, report: Report):
        tpl_path = Path(env.TEMPLATE_PATH)
        tpl_env = Environment(
            loader=FileSystemLoader(tpl_path.parent)
        )
        template = tpl_env.get_template(tpl_path.name)
        adoc = template.render(
            {
                "report": report,
                "query": self.query
            }
        )
        self._save(adoc)
