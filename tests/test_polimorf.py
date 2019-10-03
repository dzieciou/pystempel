from stempel import StempelStemmer

def test_polimorf():
    stemmer = StempelStemmer.from_file('../data/stemmer_polimorf.tbl')
    assert stemmer.stem('jabłkami') == 'jabłko'
