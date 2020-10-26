# MIT License
# Copyright (c) 2019, INRIA
# Copyright (c) 2019, University of Lille
# All rights reserved.
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import pytest
import pymongo


from pyJoules.energy_trace import EnergySample, EnergyTrace
from pyJoules.handler.mongo_handler import MongoHandler, MongoInitError


URI = 'mongodb://localhost:27017'
DATABASE_NAME = 'test_pyjoules_db'
COLLECTION_NAME = 'test_pyjoules_col'


def clean_database(uri):
    """
    drop test_pyjoules_* collections
    """
    mongo = pymongo.MongoClient(uri)
    db_names = mongo.list_database_names()
    for name in db_names:
        if "test_pyjoules_" in name:
            for col in mongo[name].list_collection_names():
                mongo[name][col].drop()
    mongo.close()


@pytest.fixture
def sample1():
    return EnergySample(1, 'sample1', 2, {'d1': 1, 'd2': 2})


@pytest.fixture
def sample2():
    return EnergySample(2, 'sample2', 3, {'d1': 3, 'd2': 4})


@pytest.fixture
def trace1(sample1):
    return EnergyTrace([sample1])


@pytest.fixture
def trace2(sample1, sample2):
    return EnergyTrace([sample1, sample2])


@pytest.fixture
def database():
    yield pymongo.MongoClient(URI)
    clean_database(URI)


def test_create_mongo_handler_with_bad_uri_must_raise_MongoInitError(database):
    with pytest.raises(MongoInitError):
        MongoHandler('mong://toto', DATABASE_NAME, COLLECTION_NAME)


def test_create_mongo_handler_with_unreachable_host_must_raise_MongoInitError(database):
    with pytest.raises(MongoInitError):
        MongoHandler('mongodb://invalid_uri_pyjoules', DATABASE_NAME, COLLECTION_NAME, connected_timeout=100)


def test_process_one_trace_and_record_produce_a_collection_with_one_item(database, trace1):
    handler = MongoHandler(URI, DATABASE_NAME, COLLECTION_NAME)
    handler.process(trace1)
    handler.save_data()

    assert database[DATABASE_NAME][COLLECTION_NAME].count_documents({}) == 1

def test_process_one_trace_and_record_two_times_must_produce_a_collection_with_two_item(database, trace1):
    handler = MongoHandler(URI, DATABASE_NAME, COLLECTION_NAME)
    handler.process(trace1)
    handler.save_data()

    handler.process(trace1)
    handler.save_data()

    assert database[DATABASE_NAME][COLLECTION_NAME].count_documents({}) == 2


def test_process_one_trace_and_record_two_times_must_produce_a_collection_with_two_item_with_different_trace_name(database, trace1):
    handler = MongoHandler(URI, DATABASE_NAME, COLLECTION_NAME)
    handler.process(trace1)
    handler.save_data()

    handler.process(trace1)
    handler.save_data()

    traces = database[DATABASE_NAME][COLLECTION_NAME].find()

    assert traces[0]['name'] != traces[1]['name']


def test_process_one_trace_and_record_must_produce_a_collection_with_one_item_with_correct_values(database, trace1, sample1):
    handler = MongoHandler(URI, DATABASE_NAME, COLLECTION_NAME)
    handler.process(trace1)
    handler.save_data()

    traces = database[DATABASE_NAME][COLLECTION_NAME].find()

    assert traces[0]['name'] == 'trace_0'
    assert traces[0]['trace'][0]['timestamp'] == sample1.timestamp
    assert traces[0]['trace'][0]['tag'] == sample1.tag
    assert traces[0]['trace'][0]['duration'] == sample1.duration
    assert traces[0]['trace'][0]['energy'] == sample1.energy


def test_process_two_trace_and_record_must_produce_a_collection_with_two_item_with_correct_values(database, sample1, sample2):
    handler = MongoHandler(URI, DATABASE_NAME, COLLECTION_NAME)
    handler.process([sample1])
    handler.save_data()

    handler.process([sample2])
    handler.save_data()

    traces = database[DATABASE_NAME][COLLECTION_NAME].find()

    assert traces[0]['name'] == 'trace_0'
    assert traces[0]['trace'][0]['timestamp'] == sample1.timestamp
    assert traces[0]['trace'][0]['tag'] == sample1.tag
    assert traces[0]['trace'][0]['duration'] == sample1.duration
    assert traces[0]['trace'][0]['energy'] == sample1.energy

    assert traces[1]['name'] == 'trace_1'
    assert traces[1]['trace'][0]['timestamp'] == sample2.timestamp
    assert traces[1]['trace'][0]['tag'] == sample2.tag
    assert traces[1]['trace'][0]['duration'] == sample2.duration
    assert traces[1]['trace'][0]['energy'] == sample2.energy
