import argparse
from datetime import date
from arxivtrend.domain.services import ArxivApi, Query


def parse_date_str(date_str: str) -> date:
    try:
        return date.fromisoformat(date_str)
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            str(e) + " Date must be in ISO format. ex. 2020-01-01"
        )


parser = argparse.ArgumentParser()
parser.add_argument(
    "q", type=str,
    help='search query'
)
parser.add_argument(
    "-e", "--submitted_end",
    type=parse_date_str, required=False
)
parser.add_argument(
    "-b", "--submitted_begin",
    type=parse_date_str, required=False
)
parser.add_argument(
    "-c", "--category",
    type=str, required=False
)


if __name__ == "__main__":
    args = parser.parse_args()
    q = Query(
        search_q=args.q,
        submitted_begin=args.submitted_begin,
        submitted_end=args.submitted_end,
        category=args.category
    )
    api = ArxivApi()

    results = api.search(
        q,
        max_results=10
    )

    for s in results:
        print(s.title)
        print(s.categories)
        print(s.summary)
        print(s.published)
        print("")
