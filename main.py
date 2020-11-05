from sources.parsedocument import ParseDocument as Parse
import sys
import os
import time


def main():
    # menu
    if len(sys.argv) != 5:
        print('python3 main.py choice k threshold directory')
        print('')
        print(
            'choices : 0 for compareSet,'
            ' 1 for minHashing + compareSignatures,'
            ' 2 for minHashing + LSH + compareSignatures,'
            ' 3 for all')
        print('')
        print('k for length of shinglings')
        print('')
        print('threshold for similarity')
        print('')
        print('directory with documents')
        print('')
        print('example : python3 main.py 0 5 0.8 data/')
        sys.exit()

    # get args
    choice = int(sys.argv[1])
    k = int(sys.argv[2])
    threshold = float(sys.argv[3])
    DIR = str(sys.argv[4])

    # create set of hashed shinblings and filenames is just a list with the filenames
    set_shinblings, filenames = create_shinblings(DIR, k)
    # number of shinglings
    total_shinglings = sum([len(x) for x in set_shinblings])

    print('')
    print('number of documents : {}, number of {}_shinglings: {}'.format(len(filenames), k, total_shinglings))
    print('')
    print('####################################################################################')

    if choice == 0:
        start_time = time.time()
        # print the results of compare_sets if less more threshold
        compare_set_print(set_shinblings, threshold, filenames)
        print('')
        print('execution time for compareSets = {} seconds'.format(time.time() - start_time))

    if choice == 1:
        # create hash functions, default number is set to 100
        hash_functions = Parse.create_hash_functions()
        start_time = time.time()
        # create list of signatures from set of shinblings
        set_signatures = create_signatures(set_shinblings, hash_functions)
        # print the results of compare_signatures if more than threshold
        compare_signatures_print(set_signatures, threshold, filenames)
        print('')
        print('execution time for minHashing + compareSignatures = {} seconds'.format(time.time() - start_time))

    if choice == 2:
        # create hash functions, default number is set to 100
        hash_functions = Parse.create_hash_functions()
        start_time = time.time()
        # create list of signatures from set of shinblings
        set_signatures = create_signatures(set_shinblings, hash_functions)
        # create set of candidates
        set_lsh_candidates = Parse.locality_sensitive_hashing(set_signatures)
        # print candidates
        candidates_lsh_print(set_lsh_candidates, filenames)
        print('')
        # print the results of compare_signatures for candidates if more than threshold
        compare_lsh_print(set_lsh_candidates, set_signatures, threshold, filenames)
        print('')
        print('execution time for minHashing + LSH + compareSignatures = {} seconds'.format(time.time() - start_time))

    if choice == 3:
        # create hash functions, default number is set to 100
        hash_functions = Parse.create_hash_functions()

        start_time = time.time()
        # print the results of compare_sets if more than threshold
        compare_set_print(set_shinblings, threshold, filenames)
        print('')
        print('execution time for compareSets = {} seconds'.format(time.time() - start_time))
        print('####################################################################################')

        start_time = time.time()
        # print the results of compare_signatures if more than threshold
        set_signatures = create_signatures(set_shinblings, hash_functions)
        # print the results of compare_signatures if more than threshold
        compare_signatures_print(set_signatures, threshold, filenames)
        print('')
        print('execution time for minHashing + compareSignatures = {} seconds'.format(time.time() - start_time))
        print('####################################################################################')

        start_time = time.time()
        # create list of signatures from set of shinblings
        set_signatures = create_signatures(set_shinblings, hash_functions)
        # create set of candidates
        set_lsh_candidates = Parse.locality_sensitive_hashing(set_signatures)
        # print the results of compare_signatures for candidates if more than threshold
        compare_lsh_print(set_lsh_candidates, set_signatures, threshold, filenames)
        print('')
        print('execution time for minHashing + LSH + compareSignatures = {} seconds'.format(time.time() - start_time))
        print('####################################################################################')


def create_shinblings(DIR, k):
    set_shinblings = []
    filenames = []
    for filename in os.listdir(DIR):
        file = Parse(DIR + filename)
        hashed_shinglings = file.hash_shinglings(k)
        set_shinblings.append(hashed_shinglings)
        filenames.append(filename)
    return set_shinblings, filenames


def compare_set_print(set_shinblings, threshold, filenames):
    n = len(set_shinblings)
    for i in range(n - 1):
        for y in range(i + 1, n):
            a, b = set_shinblings[i], set_shinblings[y]
            res = Parse.compare_sets(a, b)
            if res >= threshold:
                print("Similarity (compareSet) = {} for document {} and {}".format(res, filenames[i],
                                                                                   filenames[y]))


def compare_signatures_print(set_signatures, threshold, filenames):
    n = len(set_signatures)
    for i in range(n - 1):
        for y in range(i + 1, n):
            a, b = set_signatures[i], set_signatures[y]
            res = Parse.compare_signatures(a, b)
            if res >= threshold:
                print(
                    "Similarity (minHashing + compareSignatures) = {} for document {} and {}".format(res, filenames[i],
                                                                                                     filenames[y]))


def compare_lsh_print(set_lsh_candidates, set_signatures, threshold, filenames):
    for couple in set_lsh_candidates:
        x, y = couple
        a, b = set_signatures[x], set_signatures[y]
        res = Parse.compare_signatures(a, b)
        if res >= threshold:
            print("Similarity (minHashing + LSH + compareSignatures) = {} for document {} and {}".format(res,
                                                                                                         filenames[x],
                                                                                                         filenames[y]))


def candidates_lsh_print(set_lsh_candidates, filenames):
    i = 0
    for couple in set_lsh_candidates:
        x, y = couple
        print("Candidates{} = {} and {}".format(i, filenames[x], filenames[y]))
        i += 1


def create_signatures(set_shinblings, hash_functions):
    return [Parse.min_hashing(set_shinblings[i], hash_functions) for i
            in
            range(len(set_shinblings))]


if __name__ == '__main__':
    main()
