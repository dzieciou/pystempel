from collections import defaultdict

from smart_open import open


def load_morfeusz2_dict(fpath):
    with open(fpath, 'r', encoding='utf-8') as lines:
        for _ in range(40):  # FIXME improve
            next(lines)
        dict = defaultdict(list)
        for line in lines:
            orth, lemma, *rest = line.split('\t', 2)
            dict[lemma].append(orth)
    return dict


def save_dict(dict, fpath):
    with open(fpath, 'w', encoding='utf-8') as f:
        for lemma, forms in dict.items():
            if len(forms) >= 4 and len(lemma) < 9 and lemma[0].islower():
                f.write('{} {}\n'.format(lemma, ' '.join(forms)))


if __name__ == '__main__':
    dict = load_morfeusz2_dict('dicts/polimorf-20190818.tab.gz')
    save_dict(dict, 'rules.txt')
