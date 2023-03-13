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
from pathlib import Path
from typing import Callable, Optional

AnyStemmer = Callable[[str], Optional[str]]


def get_python_stemmer(stemmer_table_fpath: Path) -> AnyStemmer:
    from pystempel import Stemmer

    return Stemmer.from_file(stemmer_table_fpath)


# noinspection PyPep8Naming,PyPep8Naming,PyPep8Naming
def get_java_stemmer(stemmer_table_fpath, jar_fpath) -> AnyStemmer:
    os.environ["CLASSPATH"] = jar_fpath

    from jnius import autoclass

    FileInputStream = autoclass("java.io.FileInputStream")
    StempelStemmer = autoclass("org.apache.lucene.analysis.stempel.StempelStemmer")
    stemmerTrie = StempelStemmer.load(FileInputStream(str(stemmer_table_fpath)))
    return StempelStemmer(stemmerTrie).stem


def load_words(dict_fpath):
    with open(dict_fpath, "rb") as f:
        for line in f:
            yield line.decode("utf-8").strip()


def find_vcs_root(test, dirs=(".git",), default=None):
    import os

    prev, test = None, os.path.abspath(test)
    while prev != test:
        if any(os.path.isdir(os.path.join(test, d)) for d in dirs):
            return Path(test)
        prev, test = test, os.path.abspath(os.path.join(test, os.pardir))
    return Path(default)


ROOT_DIR = find_vcs_root(os.path.dirname(__file__))


def get_test_data_path(fname):
    return os.path.join(ROOT_DIR, "tests", "data", fname)


def get_library_data_path(*parts):
    return (ROOT_DIR / "src" / "pystempel" / "data").joinpath(*parts)


def get_stempel_jar_path():
    return os.path.join(ROOT_DIR, "stempel-8.1.1.jar")
