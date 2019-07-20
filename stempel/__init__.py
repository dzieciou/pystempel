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

import importlib.resources as pkg_resources
from typing import List

from stempel.egothor import Trie, MultiTrie2, Diff
from stempel.streams import DataInputStream


class StempelStemmer:

    @classmethod
    def default(cls):
        """
        Construct a stemmer using default stemming trie.
        :return: stemmer instance.
        """
        return cls.from_resource('stemmer_20000.tbl')

    @classmethod
    def from_resource(cls, file):
        """
        Construct a stemmer using stemming table from a given file in the
        stempel package.
        :param file: file containing stemming trie.
        :return: stemmer instance.
        """
        with pkg_resources.open_binary('stempel', file) as inp:
            return cls.from_stream(DataInputStream(inp))

    @classmethod
    def from_file(cls, file):
        """
        Construct a stemmer using stemming table from a given file.
        :param file: file containing stemming trie.
        :return: stemmer instance.
        """
        with open(file, 'rb') as f:
            return cls.from_stream(DataInputStream(f))

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
    def __trie_from_stream(cls, inp):
        if not isinstance(inp, DataInputStream):
            raise ValueError
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

        cmd = self.stemmer_trie.get_last_on_path(word)
        if cmd is None:
            return None

        buffer = list(word)
        Diff.apply(buffer, cmd)
        return ''.join(buffer) if len(buffer) > 0 else None
