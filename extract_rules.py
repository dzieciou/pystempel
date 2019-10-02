from collections import defaultdict

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


if __name__ == '__main__':
    dict = load_morfeusz2_dict('dicts/polimorf-20190818.tab.gz')
    save_dict(dict, 'rules.txt')
