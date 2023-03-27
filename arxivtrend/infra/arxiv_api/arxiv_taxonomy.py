from typing import List
from arxivtrend.domain.repos import ArxivTaxonomyRepo
from .taxonomies import taxonomies


class ArxivTaxonomy(ArxivTaxonomyRepo):
    def get_partial_match_taxonomies(cat_q: str) -> List[str]:
        if cat_q is None or cat_q == "":
            return []

        ret = []
        for taxos in taxonomies.values():
            ret.extend([
                t for t in taxos
                if cat_q in t
            ])
        return ret
