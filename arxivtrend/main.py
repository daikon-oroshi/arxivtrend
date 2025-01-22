import click
from datetime import date
from arxivtrend.apps import SearchUsecase
from arxivtrend.domain.entities import (
    ArxivQueryEntity
)


@click.group()
def cli():
    pass


dec_search_q_arg = click.argument(
        'search_query',
        type=click.STRING,
    )


dec_begin_arg = click.option(
        '-b',
        'begin',
        type=click.DateTime(),
        default=date(1991, 1, 1),
        help='ex. 2020-01-01.'
    )


dec_end_arg = click.option(
        '-e',
        'end',
        type=click.DateTime(),
        default=date.today(),
        help='ex. 2045-12-31.'
    )


dec_category_arg = click.option(
        "-c", "--category",
        type=click.STRING,
        required=False,
        default=""
    )


dec_force_reacquire = click.option(
        "-f",
        "--force_reacquire",
        is_flag=True,
        help='force reacquisition even if arxiv data was cached.'
    )


@cli.command()
@dec_search_q_arg
@dec_begin_arg
@dec_end_arg
@dec_category_arg
@dec_force_reacquire
def search(
    search_query: str,
    begin: date | None,
    end: date | None,
    category: str,
    force_reacquire: bool = False
):
    query = ArxivQueryEntity(
        search_q=search_query,
        submitted_begin=begin,
        submitted_end=end,
        category=category
    )
    usecase = SearchUsecase()
    usecase.search_and_cache_arxiv(
        query,
        force_reacquire
    )


@cli.command()
@dec_search_q_arg
@dec_begin_arg
@dec_end_arg
@dec_category_arg
def delete(
    q: str,
    begin: date | None,
    end: date | None,
    category: str,
):
    query = ArxivQueryEntity(
        search_q=q,
        submitted_begin=begin,
        submitted_end=end,
        category=category
    )
    usecase = SearchUsecase()
    usecase.delete_cache(query)


@cli.command()
def delete_all():
    usecase = SearchUsecase()
    usecase.delete_cache_all()


def create_report():
    pass


if __name__ == "__main__":
    cli()
