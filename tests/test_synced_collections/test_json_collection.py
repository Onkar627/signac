# Copyright (c) 2020 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.
import json
import os

import pytest
from attr_dict_test import AttrDictTest, AttrListTest
from synced_collection_test import SyncedDictTest, SyncedListTest

from signac.synced_collections.backends.collection_json import (
    JSONAttrDict,
    JSONAttrList,
    JSONDict,
    JSONList,
)


class JSONCollectionTest:

    _write_concern = False
    _fn = "test.json"

    def store(self, synced_collection, data):
        with open(synced_collection.filename, "wb") as f:
            f.write(json.dumps(data).encode())

    @pytest.fixture
    def synced_collection(self, tmpdir):
        yield self._collection_type(
            filename=os.path.join(tmpdir, self._fn),
            write_concern=self._write_concern,
        )

    @pytest.fixture
    def synced_collection_positional(self, tmpdir):
        """Fixture that initializes the object using positional arguments."""
        yield self._collection_type(
            os.path.join(tmpdir, "test2.json"), self._write_concern
        )

    def test_filename(self, synced_collection):
        assert os.path.basename(synced_collection.filename) == self._fn


class TestJSONDict(JSONCollectionTest, SyncedDictTest):

    _collection_type = JSONDict

    # The following test tests the support for non-str keys
    # for JSON backend which will be removed in version 2.0.
    # See issue: https://github.com/glotzerlab/signac/issues/316.
    def test_keys_non_str_valid_type(self, synced_collection, testdata):
        for key in (0, None, True):
            with pytest.deprecated_call(match="Use of.+as key is deprecated"):
                synced_collection[key] = testdata
            assert str(key) in synced_collection
            assert synced_collection[str(key)] == testdata


class TestJSONList(JSONCollectionTest, SyncedListTest):

    _collection_type = JSONList


class TestJSONDictWriteConcern(TestJSONDict):
    _write_concern = True


class TestJSONListWriteConcern(TestJSONList):
    _write_concern = True


class TestJSONAttrDict(TestJSONDict, AttrDictTest):

    _collection_type = JSONAttrDict


class TestJSONAttrList(TestJSONList, AttrListTest):

    _collection_type = JSONAttrList
