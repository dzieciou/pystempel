from stempel import StempelStemmer

def test_polimorf():
    stemmer = StempelStemmer.polimorf()
    while True:
        form = input('Enter some form:')
        print(stemmer.stem(form))


test_polimorf()