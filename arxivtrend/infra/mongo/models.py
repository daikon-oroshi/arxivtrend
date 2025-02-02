from mongoengine import (
    Document, StringField,
    DateTimeField,
    ListField, ReferenceField,
    PULL, DictField, ValidationError
)
from arxivtrend.domain.entities import (
    ArxivSummaryEntity, ArxivResultEntity,
    ArxivQuery, Token
)


class TokenFiled(DictField):
    def validation(self, value: dict):
        if set(value.keys()) != {"word", "pos"}:
            raise ValidationError(f"Invalid token value: {value}")


class ArxivSummary(Document):
    entry_id = StringField(max_length=200, required=True)
    updated = DateTimeField()
    published = DateTimeField()
    title = StringField()
    authors = ListField(StringField())
    summary = StringField()
    categories = ListField(StringField())
    tokens = ListField(TokenFiled())

    meta = {
        'ordering': ['entry_id'],
    }

    @staticmethod
    def from_entity(
        entity: ArxivSummaryEntity
    ) -> "ArxivSummary":
        return ArxivSummary(
            entry_id=entity.entry_id,
            updated=entity.updated,
            published=entity.published,
            title=entity.title,
            authors=entity.authors,
            summary=entity.summary,
            categories=entity.categories,
            tokens=[
                t.model_dump() for t in entity.tokens
            ]
        )

    def to_entity(
        self
    ) -> ArxivSummaryEntity:
        summary = ArxivSummaryEntity(
            entry_id=self.entry_id,
            updated=self.updated,
            published=self.published,
            title=self.title,
            authors=self.authors,
            summary=self.summary,
            categories=self.categories,
            tokens=[
                Token(**t) for t in self.tokens
            ]
        )
        return summary


class ArxivResult(Document):
    search_q = StringField(max_length=200, required=True)
    submitted_begin = DateTimeField()
    submitted_end = DateTimeField()
    category = StringField(max_length=200, required=True)
    summaries = ListField(
        ReferenceField(ArxivSummary),
        reverse_delete_rule=PULL
    )

    meta = {
        'indexes': [
            {
                'fields': ['$search_q', '$category'],
                'unique': True
            }
        ]
    }

    @staticmethod
    def from_query_entity(
        entity: ArxivQuery,
    ) -> "ArxivResult":
        return ArxivResult(
            search_q=entity.search_q,
            submitted_begin=entity.submitted_begin,
            submitted_end=entity.submitted_end,
            category=entity.category,
            summaries=[]
        )

    @staticmethod
    def from_entity(
        entity: ArxivResultEntity,
    ) -> "ArxivResult":
        ret = ArxivResult.from_query_entity(entity.query)
        ret.summaries = [
            ArxivSummary.from_entity(r)
            for r in entity.results
        ]
        return ret

    def to_entity(
        self
    ) -> ArxivResultEntity:
        return ArxivResultEntity(
            query=ArxivQuery(
                search_q=self.search_q,
                submitted_begin=self.submitted_begin,
                submitted_end=self.submitted_end,
                category=self.category,
            ),
            results=[
                ArxivSummary.to_entity(s)
                for s in self.summaries
            ]
        )
