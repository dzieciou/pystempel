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
import shutil
import subprocess
from pathlib import Path

import morfeusz2


def save_dict(dict, fpath):
    with open(fpath, "w", encoding="utf-8") as f:
        for lemma, forms in dict.items():
            # Exclude proper names and lemmas with few forms
            if lemma[0].islower() and len(forms) >= 4:
                f.write("{} {}\n".format(lemma, " ".join(forms)))


def extract_rules(dict_fpath, rule_fpath):
    dict = morfeusz2.load_dict(dict_fpath)
    save_dict(dict, rule_fpath)


def compile_stemmer_table(jar_fpath, algorithm, rules_fpath):
    os.environ["CLASSPATH"] = jar_fpath

    subprocess.run(
        [
            "java",
            "-cp",
            jar_fpath,
            # To avoid JavaHeapSpace when loading rules into memory.
            "-Xms16m",
            "-Xmx6144m",
            # To avoid StackOverflowException because of excessive
            # recursion.
            "-Xss8m",
            "org.egothor.stemmer.Compile",
            algorithm,
            rules_fpath,
        ]
    )


def extract_compile(dict_fpath, stemmer_tbl_fpath):
    extract_rules(dict_fpath, "rules.txt")
    compile_stemmer_table(
        "stempel-8.1.1.jar", algorithm="-0ME2", rules_fpath="rules.txt"
    )
    assert Path("rules.txt.out").exists()
    os.replace("rules.txt.out", stemmer_tbl_fpath)


if __name__ == "__main__":
    extract_compile("dicts/polimorf-20190818.tab.gz", "stempel/stemmer_polimorf.tbl")
    with open("pystempel/stemmer_polimorf.tbl", "rb") as f_in:
        with gzip.open(
                "pystempel/stemmer_polimorf.tbl.gz", mode="wb", compresslevel=9
        ) as f_out:
            shutil.copyfileobj(f_in, f_out)
