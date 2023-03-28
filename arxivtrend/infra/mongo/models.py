from mongoengine import (
    Document, StringField,
    DateTimeField,
    ListField, LazyReferenceField,
    CASCADE
)
from arxivtrend.domain.entities import (
    ArxivSummaryEntity, ArxivResultEntity,
    ArxivQueryEntity
)


class ArxivSummary(Document):
    entry_id: StringField(max_length=200, required=True)
    updated: DateTimeField()
    published: DateTimeField()
    title: StringField()
    authors: ListField(StringField())
    summary: StringField()
    categories: ListField(StringField())

    meta = {
        'ordering': ['entry_id'],
    }

    @classmethod
    def from_entity(
        cls,
        entity: ArxivSummaryEntity
    ) -> "ArxivSummary":
        return ArxivSummary(
            entry_id=entity.entry_id,
            updated=entity.updated,
            published=entity.published,
            title=entity.title,
            authors=entity.authors,
            summary=entity.summary,
            categories=entity.categories
        )

    def to_entity(
        self
    ) -> ArxivSummaryEntity:
        return ArxivSummaryEntity(
            entry_id=self.entry_id,
            updated=self.updated,
            published=self.published,
            title=self.title,
            authors=self.authors,
            summary=self.summary,
            categories=self.categories
        )


class ArxivResult(Document):
    search_q: StringField(max_length=200, required=True)
    submitted_begin: DateTimeField()
    submitted_end: DateTimeField()
    category: StringField(max_length=200, required=True)
    summaries: LazyReferenceField(
        ListField(ArxivSummary()),
        reverse_delete_rule=CASCADE
    )

    meta = {
        'indexes': [
            {
                'fields': ['search_q', 'category'],
                'unique': True
            }
        ]
    }

    @classmethod
    def from_entity(
        cls,
        entity: ArxivResultEntity
    ) -> "ArxivResult":
        return ArxivResult(
            search_q=entity.query.search_q,
            submitted_begin=entity.query.submitted_begin,
            submitted_end=entity.query.submitted_end,
            category=entity.query.category,
            summaries=[
                ArxivSummary.from_entity(r)
                for r in entity.results
            ]
        )

    def to_entity(
        self
    ) -> ArxivResultEntity:
        return ArxivResultEntity(
            query=ArxivQueryEntity(
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
