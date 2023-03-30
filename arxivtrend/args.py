import argparse
from datetime import date
from enum import Enum


class Commands(Enum):
    DEFAULT = "default"
    DELETE = "delete"
    DELETE_ALL = "delete_all"
    REPORT_ONLY = "report_only"


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
    type=str, required=False,
    default=""
)
parser.add_argument(
    "-f", "--force_reacquire",
    action='store_true',
    help='force reacquisition even if arxiv data was chaced.'
)
parser.add_argument(
    "-m", "--command",
    type=str, choices=[c.value for c in Commands],
    required=False, default="default"
)
