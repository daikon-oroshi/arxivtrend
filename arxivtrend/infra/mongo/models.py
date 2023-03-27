from mongoengine import (
    Document, StringField,
    DateTimeField,
    ListField, ReferenceField
)
from arxivtrend.domain.entities import (
    ArxivSummaryEntity, ArxivResultEntity
)


class ArxivSummaryModel(Document):
    entry_id: StringField(max_length=200, required=True)
    updated: DateTimeField()
    published: DateTimeField()
    title: StringField()
    authors: ListField(StringField())
    summary: StringField()
    categories: ListField(StringField())

    def from_entity(
        self,
        entity: ArxivSummaryEntity
    ):
        pass

    def to_entity(
        self
    ) -> ArxivSummaryEntity:
        pass


class ArxivResultModel(Document):
    search_q: StringField(max_length=200, required=True)
    submitted_begin: DateTimeField()
    submitted_end: DateTimeField()
    category: StringField(max_length=200, required=True)
    summaries: ReferenceField(
        ListField(ArxivSummaryModel())
    )

    def from_entity(
        self,
        entity: ArxivResultEntity
    ):
        pass

    def to_entity(
        self
    ) -> ArxivResultEntity:
        pass
