"""
Compile stemmer table from rules.
"""

import os
import subprocess
from pathlib import Path


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


if __name__ == '__main__':
    compile_stemmer_table('stempel-8.1.1.jar',
                          algorithm='-0ME2',
                          rules_fpath='rules.txt')
    assert Path('rules.txt.out').exists()
    os.replace('rules.txt.out', 'stempel/stemmer_polimorf.tbl')
