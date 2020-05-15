from spider_template.settings import MONGO_URI, MONGO_DB, MONGO_TEMPLATE, MONGO_ORDATA, MONGO_DUPEFILTER, MONGO_FAILED
import pymongo


class MongoAction(object):
    """
    mongo api
    """
    uri = ""
    db_name = ""
    doc_name = ""

    def __init__(self):
        self.client = pymongo.MongoClient(self.uri)
        self.tdb = self.client[self.db_name]
        self.table = self.tdb[self.doc_name]

    def find(self, *args, **kwargs):
        return self.table.find(*args, **kwargs)

    def find_one(self, filter, *args, **kwargs):
        return self.table.find_one(filter, *args, **kwargs)

    def update(self, spec, document, upsert=False, manipulate=False, multi=False, check_keys=True, **kwargs):
        return self.table.update(spec, document, upsert, manipulate, multi, check_keys, **kwargs)

    def update_one(self, filter, update, upsert=False, bypass_document_validation=False, collation=None,
                   array_filters=None, session=None):
        return self.table.update_one(filter, update, upsert, bypass_document_validation,
                                     collation, array_filters, session)

    def insert(self, doc_or_docs, manipulate=True, check_keys=True, continue_on_error=False, **kwargs):
        self.table.insert(doc_or_docs, manipulate, check_keys, continue_on_error, **kwargs)

    def insert_one(self, document, bypass_document_validation=False, session=None):
        self.table.insert_one(document, bypass_document_validation, session)

    def close(self):
        self.client.close()


class TemplateInfo(MongoAction):
    uri = MONGO_URI
    db_name = MONGO_DB
    doc_name = MONGO_TEMPLATE


class OriginalData(MongoAction):
    uri = MONGO_URI
    db_name = MONGO_DB
    doc_name = MONGO_ORDATA


class FailedData(MongoAction):
    uri = MONGO_URI
    db_name = MONGO_DB
    doc_name = MONGO_FAILED


class DupeFilter(MongoAction):
    uri = MONGO_URI
    db_name = MONGO_DB
    doc_name = MONGO_DUPEFILTER
