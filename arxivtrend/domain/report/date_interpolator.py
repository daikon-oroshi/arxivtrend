from typing import List, Generator
from datetime import date
from dateutil.relativedelta import relativedelta, MO


# 日付の補完
class DateInterpolator():

    def date_generator(
        self,
        begin: date,
        delta: relativedelta
    ) -> Generator[date, None, None]:
        current = begin
        while True:
            yield current
            current = current + delta

    def interpolate(
        self,
        begin: date,
        end: date,
        span: str = "year"
    ) -> List[date]:
        if span not in ["year", "month", "week"]:
            raise ValueError(
                f"input: {span}. span must be 'year', 'month' or 'week'."
            )

        if span == "year":
            _begin = begin + relativedelta(month=1, day=1)  # 年始
            date_gen = self.date_generator(
                _begin,
                relativedelta(years=1)
            )
        elif span == "month":
            _begin = begin + relativedelta(day=1)  # 月初
            date_gen = self.date_generator(
                _begin,
                relativedelta(months=1)
            )
        else:
            _begin = begin + relativedelta(weekday=MO(-1))  # 一つ前の月曜
            date_gen = self.date_generator(
                _begin,
                relativedelta(weeks=1)
            )

        ret = []
        for d in date_gen:
            ret.append(d)
            if end <= d:
                break
        return ret
