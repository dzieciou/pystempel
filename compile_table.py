"""
Compile stemmer table from rules.
"""

import os
from pathlib import Path

def compile_stemmer_table(jar_fpath, algorithm, rules_fpath):
    os.environ['CLASSPATH'] = jar_fpath

    from jnius import autoclass

    Compile = autoclass('org.egothor.stemmer.Compile')
    Compile.main([algorithm, rules_fpath])

if __name__ == '__main__':
    compile_stemmer_table('stempel-8.1.1.jar',
                          algorithm='-0M',
                          rules_fpath='rules.txt')
    assert Path('rules.txt.out').exists()
    os.replace('rules.txt.out', 'stempel/stemmer_polimorf.tbl')