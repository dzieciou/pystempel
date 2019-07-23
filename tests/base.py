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
