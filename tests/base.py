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


def get_python_stemmer(stemmer_table_fpath):
    from stempel import StempelStemmer
    return StempelStemmer.from_file(stemmer_table_fpath)


# noinspection PyPep8Naming,PyPep8Naming,PyPep8Naming
def get_java_stemmer(stemmer_table_fpath, jar_fpath):
    os.environ['CLASSPATH'] = jar_fpath

    from jnius import autoclass

    FileInputStream = autoclass('java.io.FileInputStream')
    StempelStemmer = autoclass(
        'org.apache.lucene.analysis.stempel.StempelStemmer')
    stemmerTrie = StempelStemmer.load(FileInputStream(stemmer_table_fpath))
    return StempelStemmer(stemmerTrie)


def load_words(dict_fpath):
    with open(dict_fpath, 'rb') as f:
        for line in f:
            yield line.decode('utf-8').strip()
