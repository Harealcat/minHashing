import random
from cityhash import CityHash32


class ParseDocument:
    document = ""

    def __init__(self, path_document):
        self.document = path_document

    # create k_shinglings set from a document
    def shinglings(self, k):

        # create a set that will contain the shinglings
        k_shinglings = set()

        # open and read document
        with open(self.document) as file:
            # remove multiple whitespaces and \n
            text = ''.join(file.readlines())
            space_text = ' '.join(text.split())
            clean_text = space_text.replace('\n', '')

            n = len(clean_text)

            # add the shinglings to the set, if element already in set, add function doesn't add it
            for i in range(0, n - k - 1):
                k_shinglings.add(clean_text[i:i + k])

            # close the file
            file.close()
        return k_shinglings

    # create hashed k_shinglings from a document
    def hash_shinglings(self, k):

        # create shinglings of the document and a new set for hashed shinglings
        k_shinglings = self.shinglings(k)
        hashed_k_shinglings = set()

        # iterate shinglings
        for shinglings in k_shinglings:
            # hash shinglings to an integer (4 bytes)
            hashed_shinglings = CityHash32(shinglings)
            # add it to set
            hashed_k_shinglings.add(hashed_shinglings)

        return hashed_k_shinglings

    # compute Jaccard Similarity
    @staticmethod
    def compare_sets(x, y):
        # We use built-in python functions intersection and union for sets and we round the ratio up to 2 decimals
        return round(len(x.intersection(y)) / len(x.union(y)), 2)

    # compute minhashing with a list of hash functions and a hashed set of k_shinglings
    @staticmethod
    def min_hashing(hashed_k_shinglings, hash_functions):

        # max_size is max integer
        max_size = 2 ** 32 - 1

        # prime is prime number closest to max_size
        prime = 4294967311

        # signature will contain our signature
        signature = []
        n_hash = len(hash_functions)

        # for each hash function in hash_functions
        for i in range(n_hash):

            # current min set to max_size
            h_min = max_size
            # get a, b coeff from hi
            (a, b) = hash_functions[i]

            # for each hashed shinglings in the set
            for shingling in hashed_k_shinglings:

                # compute hi(shinglings)
                h = (a * shingling + b) % prime

                # if result is less than current hmin, update hmin
                if h < h_min:
                    h_min = h
            # add hi min tyo signature
            signature.append(h_min)
        return signature

    # create random hash functions
    @staticmethod
    def create_hash_functions(n_hash=100):

        # max_size is max integer
        max_size = 2 ** 32 - 1

        # a and b will contain our coeffs
        a, b = [], []

        i = 0
        # each coeff in a will be different from each other, same for b
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

        # return array with our coeffs, understand that array[i] = (ai, bi)
        return [(a[i], b[i]) for i in range(n_hash)]

    # compare two signatures
    @staticmethod
    def compare_signatures(x, y):

        # res is the number of similarities
        res, n = 0, len(x)

        # for each element of signature
        for i in range(n):

            # add 1 to res if the two signatures of similar for element i
            if x[i] == y[i]:
                res += 1

        # return ratio between number of similarities and number of elements in signature
        return res / n
