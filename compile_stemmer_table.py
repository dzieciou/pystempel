"""
Compile stemmer table from rules.
"""

import gzip
import os
import shutil
import subprocess
from collections import defaultdict
from pathlib import Path

from smart_open import open


def load_morfeusz2_dict(fpath):
    def skip_comments(f):
        comments = 0
        while comments < 3:
            line = f.readline()
            if line.startswith('#'):
                comments += 1

    with open(fpath, 'r', encoding='utf-8') as lines:
        skip_comments(lines)
        dict = defaultdict(list)
        for line in lines:
            orth, lemma, *rest = line.split('\t', 2)
            dict[lemma].append(orth)
    return dict


def save_dict(dict, fpath):
    with open(fpath, 'w', encoding='utf-8') as f:
        for lemma, forms in dict.items():
            # Exclude proper names and lemmas with few forms
            if lemma[0].islower() and len(forms) >= 4:
                f.write('{} {}\n'.format(lemma, ' '.join(forms)))


def extract_rules(dict_fpath, rule_fpath):
    dict = load_morfeusz2_dict(dict_fpath)
    save_dict(dict, rule_fpath)


def compile_stemmer_table(jar_fpath, algorithm, rules_fpath):
    os.environ['CLASSPATH'] = jar_fpath

    subprocess.run(['java',
                    '-cp', jar_fpath,
                    # To avoid JavaHeapSpace when loading rules into memory.
                    '-Xms16m', '-Xmx6144m',
                    # To avoid StackOverflowException because of excessive
                    # recursion.
                    '-Xss8m',
                    'org.egothor.stemmer.Compile',
                    algorithm,
                    rules_fpath])


def extract_compile(dict_fpath, stemmer_tbl_fpath):
    extract_rules(dict_fpath, 'rules.txt')
    compile_stemmer_table('stempel-8.1.1.jar',
                          algorithm='-0ME2',
                          rules_fpath='rules.txt')
    assert Path('rules.txt.out').exists()
    os.replace('rules.txt.out', stemmer_tbl_fpath)


if __name__ == '__main__':
    extract_compile('dicts/polimorf-20190818.tab.gz',
                    'stempel/stemmer_polimorf.tbl')
    with open('stempel/stemmer_polimorf.tbl', 'rb') as f_in:
        with gzip.open('stempel/stemmer_polimorf.tbl.gz',
                       mode='wb', compresslevel=9) as f_out:
            shutil.copyfileobj(f_in, f_out)
