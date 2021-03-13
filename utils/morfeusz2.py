from collections import defaultdict

from smart_open import open
from tqdm import tqdm


def load_dict(fpath):
    def skip_comments(f):
        comments = 0
        while comments < 3:
            line = f.readline()
            if line.startswith("#"):
                comments += 1

    with open(fpath, "r", encoding="utf-8") as lines:
        skip_comments(lines)
        dict = defaultdict(set)
        for line in tqdm(lines, desc="Loading dict"):
            orth, lemma, *rest = line.split("\t", 2)
            dict[lemma].add(orth)
    return dict
