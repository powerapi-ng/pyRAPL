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
import pymongo

from pyRAPL.outputs import BufferedOutput


class MongoOutput(BufferedOutput):
    """
    Store the recorded measure in a MongoDB database

    This instance act as a buffer. The method ``add`` add data to the buffer and the method ``save`` store each data
    in the buffer in the MongoDB database. After that, the buffer is flushed

    :param uri: uri used to connect to the mongoDB instance
    :param database: database name to store the data
    :param collection: collection name to store the data
    """
    def __init__(self, uri: str, database: str, collection: str):
        """
        Export the results to a collection in a mongo database
        """
        BufferedOutput.__init__(self)
        self._client = pymongo.MongoClient(uri)
        self._db = self._client[database]
        self._collection = self._db[collection]

    def _output_buffer(self):
        """
        Store all the data contained in the buffer

        :param data: data to output
        """
        self._collection.insert_many(self._buffer)
