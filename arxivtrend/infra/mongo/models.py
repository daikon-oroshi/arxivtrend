from mongoengine import (
    Document, StringField,
    DateTimeField,
    ListField, ReferenceField
)


class Summary(Document):
    entry_id: StringField(max_length=200, required=True)
    updated: DateTimeField()
    published: DateTimeField()
    title: StringField()
    authors: ListField(StringField())
    summary: StringField()
    categories: ListField(StringField())


class SearchResult(Document):
    search_q: StringField(max_length=200, required=True)
    submitted_begin: DateTimeField()
    submitted_end: DateTimeField()
    category: StringField(max_length=200, required=True)
    summaries: ReferenceField(
        ListField(Summary())
    )
