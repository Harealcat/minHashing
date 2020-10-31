from parseDocument import ParseDocument
import sys
import os


def main():
    if len(sys.argv) != 5:
        print('python3 main.py choice k threshold directory')
        print('choice : 0 for compareSet, 1 for compareSignatures, 2 for both')
        print('k for length of shinglings')
        print('threshold for similarity')
        print('directory with documents')
        print('')
        print('example : python3 main.py 0 5 0.8 data/')
        sys.exit()

    choice = int(sys.argv[1])
    k = int(sys.argv[2])
    threshold = float(sys.argv[3])
    DIR = str(sys.argv[4])

    if choice == 0:
        set_shinblings = create_shinblings(DIR, k)
        compare_set_print(set_shinblings, threshold)

    if choice == 1:
        set_shinblings = create_shinblings(DIR, k)
        hash_functions = ParseDocument.create_hash_functions()
        set_signatures = create_signatures(set_shinblings, hash_functions)
        compare_signatures_print(set_signatures, threshold)

    if choice == 2:
        set_shinblings = create_shinblings(DIR, k)
        hash_functions = ParseDocument.create_hash_functions()
        set_signatures = create_signatures(set_shinblings, hash_functions)
        compare_set_print(set_shinblings, threshold)
        compare_signatures_print(set_signatures, threshold)


def create_shinblings(DIR, k):
    set_shinblings = []
    for filename in os.listdir(DIR):
        file = ParseDocument(DIR + filename)
        hashed_shinglings = file.hash_shinglings(k)
        set_shinblings.append((hashed_shinglings, filename))
    return set_shinblings


def compare_set_print(set_shinblings, threshold):
    n = len(set_shinblings)
    for i in range(n - 1):
        for y in range(i + 1, n):
            a, b = set_shinblings[i][0], set_shinblings[y][0]
            res = ParseDocument.compare_sets(a, b)
            if res > threshold:
                print("Similarity (compareSet) = {} for document {} and {}".format(res, set_shinblings[i][1],
                                                                                   set_shinblings[y][1]))


def compare_signatures_print(set_signatures, threshold):
    n = len(set_signatures)
    for i in range(n - 1):
        for y in range(i + 1, n):
            a, b = set_signatures[i][0], set_signatures[y][0]
            res = ParseDocument.compare_signatures(a, b)
            if res > threshold:
                print("Similarity (compareSignatures) = {} for document {} and {}".format(res, set_signatures[i][1],
                                                                                          set_signatures[y][1]))


def create_signatures(set_shinblings, hash_functions):
    return [(ParseDocument.min_hashing(set_shinblings[i][0], hash_functions), set_shinblings[i][1]) for i
            in
            range(len(set_shinblings))]


if __name__ == '__main__':
    main()
