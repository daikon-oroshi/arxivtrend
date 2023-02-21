import arxiv
import argparse
from datetime import date


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


def validate_arg(args):
    pass


if __name__ == "__main__":
    args = parser.parse_args()

    search = arxiv.Search(
        query=f"ti:\"{args.q}\" AND cat:\"math.MP\" AND submittedDate:[20230215000000 TO 20230219000000]",
        sort_by=arxiv.SortCriterion.SubmittedDate,
        max_results=15
    )

    for s in search.results():
        print(s.title)
        print(s.categories)
        print(s.summary)
        print(s.published)
        print("")
