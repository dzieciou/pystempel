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

import os

import pytest

import tests.base as base

pwd = os.path.dirname(os.path.abspath(__file__))
stemmer_table_fpath = os.path.join(pwd, '..', 'data', 'stemmer_20000.tbl')
jar_fpath = os.path.join(os.getcwd(), 'stempel-8.1.1.jar')
dict_fpath = os.path.join(pwd, 'sjp_dict.txt')

python_stemmer = base.get_python_stemmer(stemmer_table_fpath)
java_stemmer = base.get_java_stemmer(stemmer_table_fpath, jar_fpath)


@pytest.mark.parametrize("word", base.load_words(dict_fpath))
def test_stemming(word):
    python_stem = python_stemmer.stem(word)
    java_stem = java_stemmer.stem(word)
    assert (python_stem is None and java_stem is None) \
            or python_stem == java_stem.toString()
