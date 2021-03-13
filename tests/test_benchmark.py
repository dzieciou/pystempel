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

import time

from tests import base
from tests.base import get_test_data_path, get_library_data_path, get_stempel_jar_path

stemmer_table_fpath = get_library_data_path("original", "stemmer_20000.tbl")
jar_fpath = get_stempel_jar_path()
dict_fpath = get_test_data_path("sjp_dict.txt")

python_stemmer = base.get_python_stemmer(stemmer_table_fpath)
java_stemmer = base.get_java_stemmer(stemmer_table_fpath, jar_fpath)


def measure_stemming_time(stemmer, words):
    start = time.time()
    for word in words:
        stemmer(word)
    end = time.time()
    return end - start


# Loading words in memory to exclude I/O times from benchmark
words = list(base.load_words(dict_fpath))

port_time = measure_stemming_time(python_stemmer, words)
wrapper_time = measure_stemming_time(java_stemmer, words)

print("Words: %d".format(len(words)))
print(
    "Python port stemming time: %f "
    "(%f/word) ".format(port_time, port_time / len(words))
)
print(
    "    Wrapper stemming time: %f "
    "(%f/word) ".format(wrapper_time, wrapper_time / len(words))
)
