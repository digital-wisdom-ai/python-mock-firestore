from unittest import TestCase

from google.cloud.firestore_v1 import FieldFilter

from mockfirestore import MockFirestore


class TestWhereField(TestCase):
    def test_collection_whereEquals(self):
        fs = MockFirestore()
        fs._data = {'foo': {
            'first': {'valid': True},
            'second': {'gumby': False}
        }}

        docs = list(fs.collection('foo').where(field='valid', op='==', value=True).stream())
        self.assertEqual({'valid': True}, docs[0].to_dict())

    def test_collection_whereEquals_with_filter(self):
        fs = MockFirestore()
        fs._data = {'foo': {
            'first': {'valid': True},
            'second': {'gumby': False}
        }}

        docs = list(fs.collection('foo').where(filter=FieldFilter('valid', '==', True)).stream())
        self.assertEqual({'valid': True}, docs[0].to_dict())
    
    def test_collection_whereNotEquals(self):
        fs = MockFirestore()
        fs._data = {'foo': {
            'first': {'count': 1},
            'second': {'count': 5}
        }}

        docs = list(fs.collection('foo').where('count', '!=', 1).stream())
        self.assertEqual({'count': 5}, docs[0].to_dict())

    def test_collection_whereLessThan(self):
        fs = MockFirestore()
        fs._data = {'foo': {
            'first': {'count': 1},
            'second': {'count': 5}
        }}

        docs = list(fs.collection('foo').where('count', '<', 5).stream())
        self.assertEqual({'count': 1}, docs[0].to_dict())

    def test_collection_whereLessThanOrEqual(self):
        fs = MockFirestore()
        fs._data = {'foo': {
            'first': {'count': 1},
            'second': {'count': 5}
        }}

        docs = list(fs.collection('foo').where('count', '<=', 5).stream())
        self.assertEqual({'count': 1}, docs[0].to_dict())
        self.assertEqual({'count': 5}, docs[1].to_dict())

    def test_collection_whereGreaterThan(self):
        fs = MockFirestore()
        fs._data = {'foo': {
            'first': {'count': 1},
            'second': {'count': 5}
        }}

        docs = list(fs.collection('foo').where('count', '>', 1).stream())
        self.assertEqual({'count': 5}, docs[0].to_dict())

    def test_collection_whereGreaterThanOrEqual(self):
        fs = MockFirestore()
        fs._data = {'foo': {
            'first': {'count': 1},
            'second': {'count': 5}
        }}

        docs = list(fs.collection('foo').where('count', '>=', 1).stream())
        self.assertEqual({'count': 1}, docs[0].to_dict())
        self.assertEqual({'count': 5}, docs[1].to_dict())

    def test_collection_whereMissingField(self):
        fs = MockFirestore()
        fs._data = {'foo': {
            'first': {'count': 1},
            'second': {'count': 5}
        }}

        docs = list(fs.collection('foo').where('no_field', '==', 1).stream())
        self.assertEqual(len(docs), 0)

    def test_collection_whereNestedField(self):
        fs = MockFirestore()
        fs._data = {'foo': {
            'first': {'nested': {'a': 1}},
            'second': {'nested': {'a': 2}}
        }}

        docs = list(fs.collection('foo').where('nested.a', '==', 1).stream())
        self.assertEqual(len(docs), 1)
        self.assertEqual({'nested': {'a': 1}}, docs[0].to_dict())

    def test_collection_whereIn(self):
        fs = MockFirestore()
        fs._data = {'foo': {
            'first': {'field': 'a1'},
            'second': {'field': 'a2'},
            'third': {'field': 'a3'},
            'fourth': {'field': 'a4'},
        }}

        docs = list(fs.collection('foo').where('field', 'in', ['a1', 'a3']).stream())
        self.assertEqual(len(docs), 2)
        self.assertEqual({'field': 'a1'}, docs[0].to_dict())
        self.assertEqual({'field': 'a3'}, docs[1].to_dict())

    def test_collection_whereArrayContains(self):
        fs = MockFirestore()
        fs._data = {'foo': {
            'first': {'field': ['val4']},
            'second': {'field': ['val3', 'val2']},
            'third': {'field': ['val3', 'val2', 'val1']}
        }}

        docs = list(fs.collection('foo').where('field', 'array_contains', 'val1').stream())
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0].to_dict(), {'field': ['val3', 'val2', 'val1']})

    def test_collection_whereArrayContainsAny(self):
        fs = MockFirestore()
        fs._data = {'foo': {
            'first': {'field': ['val4']},
            'second': {'field': ['val3', 'val2']},
            'third': {'field': ['val3', 'val2', 'val1']}
        }}

        contains_any_docs = list(fs.collection('foo').where('field', 'array_contains_any', ['val1', 'val4']).stream())
        self.assertEqual(len(contains_any_docs), 2)
        self.assertEqual({'field': ['val4']}, contains_any_docs[0].to_dict())
        self.assertEqual({'field': ['val3', 'val2', 'val1']}, contains_any_docs[1].to_dict())