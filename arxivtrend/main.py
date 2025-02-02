import click
from datetime import date
from arxivtrend.apps import SearchUsecase
from arxivtrend.domain.entities import (
    ArxivQuery
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
        default="1991-01-01",
        help='ex. 2020-01-01.'
    )


dec_end_arg = click.option(
        '-e',
        'end',
        type=click.DateTime(),
        default=date.today().strftime("%Y-%m-%d"),
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
@click.option(
        "-s",
        "--stop_query",
        is_flag=True,
        help='exclude search query from aggregate.'
    )
def create(
    search_query: str,
    begin: date | None,
    end: date | None,
    category: str,
    force_reacquire: bool = False,
    stop_query: bool = False
):
    query = ArxivQuery(
        search_q=search_query,
        submitted_begin=begin,
        submitted_end=end,
        category=category
    )
    usecase = SearchUsecase()
    usecase.create(
        query,
        force_reacquire,
        stop_query_word=stop_query
    )


@cli.command()
@dec_search_q_arg
@dec_begin_arg
@dec_end_arg
@dec_category_arg
def delete_cache(
    q: str,
    begin: date | None,
    end: date | None,
    category: str,
):
    query = ArxivQuery(
        search_q=q,
        submitted_begin=begin,
        submitted_end=end,
        category=category
    )
    usecase = SearchUsecase()
    usecase.delete_cache(query)


@cli.command()
def delete_cache_all():
    usecase = SearchUsecase()
    usecase.delete_cache_all()


@cli.command()
def show_categories():
    usecase = SearchUsecase()
    usecase.show_categories()


if __name__ == "__main__":
    cli()
