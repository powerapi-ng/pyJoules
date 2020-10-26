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
from typing import Dict, Iterable

try:
    import pymongo
except ImportError:
    import logging
    logging.getLogger().info("PyMongo is not installed.")

from . import EnergyHandler
from ..energy_trace import EnergySample


def sample_to_dict(sample: EnergySample) -> Dict:
    """
    convert a sample to a dictionary that could be inserted in a mongodb database
    """
    return {
        'timestamp': sample.timestamp,
        'tag': sample.tag,
        'duration': sample.duration,
        'energy': sample.energy,
    }


def trace_to_dict(trace: Iterable[EnergySample], trace_name: str) -> Dict:
    """
    convert a trace to a dictionary that could be inserted in a mongodb database
    """
    return {
        'name': trace_name,
        'trace': list(map(sample_to_dict, trace))
    }


class MongoInitError(Exception):
    """
    Exception raised when mongoHandler cant be initialized due to error while
    handling mongo database
    """


class MongoHandler(EnergyHandler):

    def __init__(self, uri: str, database_name: str, collection_name: str, connected_timeout: int = 30000, trace_name_prefix: str = 'trace_'):
        """
        Create a handler that will store data on mongo database

        :param uri: database uri using mongoDB uri format
        :param connection_timeout: Controls how long (in milliseconds) the driver will wait to find an available,
                                   appropriate server to carry out a database operation; while it is waiting, multiple
                                   server monitoring operations may be carried out, each controlled by connectTimeoutMS.
                                   Defaults to 30000 (30 seconds).
        :param trace_name_prefix: prefix of the trace name used to identify a trace in mongo database. The trace name is
                                  computed as follow : trace_name_prefix + trace_position (trace position is the
                                  position of the current trace in the trace list processed by the handler)

        """
        EnergyHandler.__init__(self)

        self.collection = None
        self.trace_id = 0
        self.trace_name_prefix = trace_name_prefix

        self._init_database(uri, connected_timeout, database_name, collection_name)

    def _init_database(self, uri, connected_timeout, database_name, collection_name):
        try:
            database = pymongo.MongoClient(uri, connectTimeoutMS=connected_timeout, serverSelectionTimeoutMS=connected_timeout)
            database.server_info()
            self._collection = database[database_name][collection_name]
        except pymongo.errors.InvalidURI:
            raise MongoInitError('invalid uri : ' + uri)
        except pymongo.errors.ServerSelectionTimeoutError as exn:
            raise MongoInitError('unreachable server : ' + uri + ' driver msg : ' + str(exn))
        except Exception as exn:
            raise MongoInitError(' driver msg : ' + str(exn))

    def save_data(self):
        """
        Save processed trace on the database
        """
        documents = []
        for trace in self.traces:
            documents.append(trace_to_dict(trace, self.trace_name_prefix + str(self.trace_id)))
            self.trace_id += 1
        self._collection.insert_many(documents)

        self.traces = []
