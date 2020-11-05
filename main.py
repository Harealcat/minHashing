from classes.parsedocument import ParseDocument as Parse
import os
import time
import argparse


def main():
    # flags and arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--choice", type=int, choices=[0, 1, 2, 3], default=2,
                        help=' 0 for compareSet,'
                             ' 1 for minHashing + compareSignatures,'
                             ' 2 for minHashing + LSH + compareSignatures,'
                             ' 3 for all,'
                             ' default = 3')
    parser.add_argument("-k", "--k", type=int, default=5, help='length of shinglings')
    parser.add_argument("-t", "--threshold", type=float, default=0.7, help='threshold for similarity')
    parser.add_argument("-n", "--nb_hash", type=int, default=100, help='number of hash functions, default=100')
    parser.add_argument("-b", "--bands", type=int, default=20, help='number of bands for LSH, default=20')
    parser.add_argument("directory", help='directory with documents')
    args = parser.parse_args()

    # get args
    choice = args.choice
    k = args.k
    threshold = args.threshold
    n_hash = args.nb_hash
    n_bands = args.bands
    DIR = str(args.directory)

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
        hash_functions = Parse.create_hash_functions(n_hash)
        start_time = time.time()
        # create list of signatures from set of shinblings
        set_signatures = create_signatures(set_shinblings, hash_functions)
        # print the results of compare_signatures if more than threshold
        compare_signatures_print(set_signatures, threshold, filenames)
        print('')
        print('execution time for minHashing + compareSignatures = {} seconds'.format(time.time() - start_time))

    if choice == 2:
        # create hash functions, default number is set to 100
        hash_functions = Parse.create_hash_functions(n_hash)
        start_time = time.time()
        # create list of signatures from set of shinblings
        set_signatures = create_signatures(set_shinblings, hash_functions)
        # create set of candidates
        set_lsh_candidates = Parse.locality_sensitive_hashing(set_signatures, n_bands)
        # print candidates
        candidates_lsh_print(set_lsh_candidates, filenames)
        print('')
        # print the results of compare_signatures for candidates if more than threshold
        compare_lsh_print(set_lsh_candidates, set_signatures, threshold, filenames)
        print('')
        print('execution time for minHashing + LSH + compareSignatures = {} seconds'.format(time.time() - start_time))

    if choice == 3:
        # create hash functions, default number is set to 100
        hash_functions = Parse.create_hash_functions(n_hash)

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
        set_lsh_candidates = Parse.locality_sensitive_hashing(set_signatures, n_bands)
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
