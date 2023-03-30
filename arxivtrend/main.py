from arxivtrend.apps import SearchUsecase
from arxivtrend.domain.entities import (
    ArxivQueryEntity
)
from arxivtrend.args import parser, Commands


def parse_search_query(args) -> ArxivQueryEntity:
    return ArxivQueryEntity(
        search_q=args.q,
        submitted_begin=args.submitted_begin,
        submitted_end=args.submitted_end,
        category=args.category
    )


def delete(args):
    query = parse_search_query(args)
    usecase = SearchUsecase()
    usecase.delete_cache(query)


def delete_all():
    usecase = SearchUsecase()
    usecase.delete_cache_all()


def search(args):
    query = parse_search_query(args)
    usecase = SearchUsecase()
    usecase.search_and_cache_arxiv(
        query, args.force_reacquire
    )


def create_report(args):
    pass


def main():
    args = parser.parse_args()
    if args.command == Commands.DELETE.value:
        delete(args)
    elif args.command == Commands.DELETE_ALL.value:
        delete_all()
    elif args.command == Commands.REPORT_ONLY.value:
        create_report(args)
    else:
        search(args)
        create_report(args)


if __name__ == "__main__":
    main()
