#!/usr/bin/env python3

import concurrent.futures
import hashlib
import os
import string
import sys
from tqdm import tqdm 

# Constants

ALPHABET = string.ascii_lowercase + string.digits

# Functions

def usage(exit_code=0):
    progname = os.path.basename(sys.argv[0])
    print(f'''Usage: {progname} [-a ALPHABET -c CORES -l LENGTH -p PATH -s HASHES]
    -a ALPHABET Alphabet to use in permutations
    -c CORES    CPU Cores to use
    -l LENGTH   Length of permutations
    -p PREFIX   Prefix for all permutations
    -s HASHES   Path of hashes file''')
    sys.exit(exit_code)

def md5sum(s):
    ''' Compute md5 digest for given string. '''
    # TODO: Use the hashlib library to produce the md5 hex digest of the given
    # string.
    s_binary = s.encode()
    md5 = hashlib.md5(s_binary).hexdigest()
    #print(f'md5: {md5}')    
    #print(len(md5))
    return md5

def permutations(length, alphabet=ALPHABET):
    ''' Recursively yield all permutations of alphabet up to given length. '''
    # TODO: Use yield to create a generator function that recursively produces
    # all the permutations of the given alphabet up to the provided length.

    if length == 1 or length == 0:
        for letter in alphabet:
            yield letter
    
    else:
        for letter in alphabet:
            for letter2 in permutations(length-1, alphabet):
                yield letter + letter2


def flatten(sequence):
    ''' Flatten sequence of iterators. '''
    # TODO: Iterate through sequence and yield from each iterator in sequence.

    for list1 in sequence:
        for item in list1: 
            yield item

def crack(hashes, length, alphabet=ALPHABET, prefix=''):
    ''' Return all password permutations of specified length that are in hashes
    by sequentially trying all permutations. '''
    # TODO: Return list comprehension that iterates over a sequence of
    # candidate permutations and checks if the md5sum of each candidate is in
    # hashes.
    list1 = [prefix + item for item in permutations(length, alphabet) if md5sum(prefix + item) in hashes]
    #print(list1)
    return list1

def whack(arguments):
    ''' Call the crack function with the specified list of arguments '''
    hashes = arguments[0]
    length = arguments[1]
    alphabet = arguments[2]
    prefix = arguments[3]
    
    crack_list = crack(hashes,length, alphabet, prefix)
    return crack_list
    '''
    for i in crack_list:
        print(i)
    return crack_list
    '''

def smash(hashes, length, alphabet=ALPHABET, prefix='', cores=1):
    ''' Return all password permutations of specified length that are in hashes
    by concurrently subsets of permutations concurrently.
    '''
    # TODO: Create generator expression with arguments to pass to whack and
    # then use ProcessPoolExecutor to apply whack to all items in expression.

    # Generator expression representing a sequence of arguments to pass
    # to `whack` (hashes, length, alphabet remain constant, but prefix
    # should change for each argument tuple).
    arguments = ((hashes, length - 1, alphabet, prefix + letter, cores) for letter in alphabet)

    # Create a ProcessPoolExecutor and then apply whack to the
    # arguments
    with concurrent.futures.ProcessPoolExecutor(cores) as executor:
        return flatten(executor.map(whack, arguments))   

# Main Execution

def main():
    arguments   = sys.argv[1:]
    alphabet    = ALPHABET
    cores       = 1
    hashes_path = 'hashes.txt'
    length      = 1
    prefix      = ''
    progress    = 0

    # TODO: Parse command line arguments

    if len(arguments) == 0:
        usage(0)

    while(len(arguments) > 0):
        argument = arguments.pop(0)
        if argument == '-a':
            alphabet = arguments.pop(0)
        elif argument == '-c':
            cores = int(arguments.pop(0))
        elif argument == '-l':
            length = int(arguments.pop(0))
        elif argument == '-p':
            prefix = arguments.pop(0)
        elif argument == '-s':
            hashes_path = arguments.pop(0)
        elif argument == '-P':
            progress == 1
        else:
            usage(1)
    '''
    print(f'alphabet: {alphabet}')
    print(f'cores: {cores}')
    print(f'length: {length}')
    print(f'prefix: {prefix}')
    print(f'hashes_path: {hashes_path}')
    '''

    md5sum('a')
 
    # TODO: Load hashes set
    
    hashes = set([line.strip() for line in open(hashes_path)] )
           
    # TODO: Execute crack or smash function
    
    #print(hashes)
    if length == 1 or cores == 1:
        all_pswds = crack(hashes, length, alphabet, prefix) 
    else:
        all_pswds = smash(hashes,length, alphabet, prefix, cores)
    #print(type(all_pswds))

    # TODO: Print all found passwords

    for item in tqdm(all_pswds):
        
        print(item)    

if __name__ == '__main__':
    main()
