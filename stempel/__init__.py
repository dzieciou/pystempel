"""
Licensed to the Apache Software Foundation (ASF) under one or more
contributor license agreements.  See the NOTICE file distributed with
this work for additional information regarding copyright ownership.
The ASF licenses this file to You under the Apache License, Version 2.0
(the "License"); you may not use this file except in compliance with
the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import gzip
import os

from stempel import egothor
from stempel.egothor import Trie, MultiTrie2
from stempel.streams import DataInputStream


class StempelStemmer:

    @classmethod
    def default(cls):
        """
        Construct a stemmer using default stemming trie.
        :return: stemmer instance.
        """
        return cls.from_resource('stemmer_20000.tbl.gz')

    @classmethod
    def polimorf(cls):
        """
        Construct a stemmer using default stemming trie.
        :return: stemmer instance.
        """
        return cls.from_resource('stemmer_polimorf.tbl.gz')

    @classmethod
    def from_resource(cls, fname):
        """
        Construct a stemmer using stemming table from a given file in the
        stempel package.
        :param file: name of file inside the library containing stemming trie.
        :return: stemmer instance.
        """
        # TODO https://setuptools.readthedocs.io/en/latest/setuptools.html#setting-the-zip-safe-flag
        package_dir = os.path.dirname(os.path.abspath(__file__))
        fpath = os.path.join(package_dir, fname)
        return cls.from_file(fpath)

    @classmethod
    def from_file(cls, fpath):
        """
        Construct a stemmer using stemming table from a given file.
        :param fpath: path to the file containing stemming trie.
        :return: stemmer instance.
        """
        if fpath.endswith('.gz'):
            file_size = get_uncompressed_size(fpath)
            with gzip.open(fpath, 'rb') as f:
                return cls.from_stream(DataInputStream(f, file_size))
        else:
            file_size = os.stat(fpath).st_size
            with open(fpath, 'rb') as f:
                return cls.from_stream(DataInputStream(f, file_size))

    @classmethod
    def from_stream(cls, stream):
        """
        Construct a stemmer using stemming table from a given stream.
        :param stream:
        :return:
        """
        stemmer_table = cls.__trie_from_stream(stream)
        return StempelStemmer(stemmer_table)

    @classmethod
    def __trie_from_stream(cls, inp: DataInputStream):
        method = inp.read_utf().upper()
        if 'M' in method:
            return MultiTrie2.from_stream(inp)
        else:
            return Trie.from_stream(inp)

    def __init__(self, stemmer_trie):
        """
        Construct a stemmer from a given trie.
        :param stemmer_trie: stemming trie.
        """
        self.stemmer_trie = stemmer_trie

    def stem(self, word):
        """
        Stem a word.
        :param word: inp word to be stemmed
        :return: stemmed word, or None if the stem could not be generated.
        """

        patch = self.stemmer_trie.get_last_on_path(word)
        if patch is None:
            return None

        buffer = list(word)
        egothor.apply_patch(buffer, patch)
        return ''.join(buffer) if len(buffer) > 0 else None

import struct

def get_uncompressed_size(fpath):
    with open(fpath, 'rb') as f:
        f.seek(-4, 2)
        return struct.unpack('I', f.read(4))[0]