import random
from cityhash import CityHash32


class ParseDocument:
    document = ""

    def __init__(self, path_document):
        self.document = path_document

    def shinglings(self, k):
        k_shinglings = set()
        with open(self.document) as file:
            text = ''.join(file.readlines())
            space_text = ' '.join(text.split())
            clean_text = space_text.replace('\n', '')
            n = len(clean_text)
            for i in range(0, n - k - 1):
                k_shinglings.add(clean_text[i:i + k])
            file.close()
        return k_shinglings

    def hash_shinglings(self, k):
        k_shinglings = self.shinglings(k)
        hashed_k_shinglings = set()
        for shinglings in k_shinglings:
            hashed_shinglings = CityHash32(shinglings)
            hashed_k_shinglings.add(hashed_shinglings)
        return hashed_k_shinglings

    @staticmethod
    def compare_sets(x, y):
        return round(len(x.intersection(y)) / len(x.union(y)), 2)

    @staticmethod
    def min_hashing(hashed_k_shinglings, hash_functions):
        max_size = 2 ** 32 - 1
        prime = 4294967311
        signature = []
        n_hash = len(hash_functions)

        for i in range(n_hash):
            h_min = max_size
            (a, b) = hash_functions[i]
            for shingling in hashed_k_shinglings:
                h = (a * shingling + b) % prime
                if h < h_min:
                    h_min = h
            signature.append(h_min)
        return signature

    @staticmethod
    def create_hash_functions(n_hash=100):
        max_size = 2 ** 32 - 1
        a, b = [], []
        i = 0
        while i != n_hash:
            new_a = random.randint(0, max_size)
            new_b = random.randint(0, max_size)
            while new_a in a:
                new_a = random.randint(0, max_size)
            while new_b in b:
                new_b = random.randint(0, max_size)
            a.append(new_a)
            b.append(new_b)
            i += 1
        return [(a[i], b[i]) for i in range(n_hash)]

    @staticmethod
    def compare_signatures(x, y):
        res, n = 0, len(x)
        for i in range(n):
            if x[i] == y[i]:
                res += 1
        return res / n
