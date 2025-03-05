import pandas as pd 
import numpy as np
import math

delta = math.exp(-5)
epsilon = math.exp(1) * (10**(-4))
numhash = math.log(1/delta) 

# Returns hash(x) for hash function given by parameters a, b, p and n_buckets
def hash_fun(a, b, p, n_buckets, x):
    y = x % p
    hash_val = (a*y + b) % p
    return hash_val % n_buckets

p = 123457
n_buckets = 10**4

hash_params = pd.read_csv("hash_params.txt", delimiter='\t', names=['a', 'b'])
hash_a = list(hash_params["a"])
hash_b = list(hash_params["b"])

from functools import partial
hash_fn_partial = partial(hash_fun, p=p, n_buckets=n_buckets)

def update_hashtable(hash_ind, fn_num, hashtab, hash_fn_inds, x):
    if hash_ind not in hashtab:
        hashtab[hash_ind] = [0]*5
    
    lst = hashtab[hash_ind]
    lst[fn_num] += 1
    hashtab[hash_ind] = lst
    
    if x not in hash_fn_inds:
        hash_fn_inds[x] = [0]*5
    
    lst = hash_fn_inds[x]
    lst[fn_num] = hash_ind
    hash_fn_inds[x] = lst

    return hashtab, hash_fn_inds

true_counts = pd.read_csv("counts.txt", delimiter='\t', names=["number", "count"])
numbers = list(true_counts['number'].astype(int))
counts = list(true_counts['count'].astype(int))

true_counts_dict = {}
for i in range(len(true_counts['number'])):
    true_counts_dict[numbers[i]] = counts[i]

words = open('words_stream.txt', 'r')
results = {}
hash_fn_inds = {}
total_word_count = 0
for line in words:
    x = int(line.strip())
    results, hash_fn_inds = update_hashtable(hash_fn_partial(x=x, a=hash_a[0], b=hash_b[0]), 0, results, hash_fn_inds, x)
    results, hash_fn_inds = update_hashtable(hash_fn_partial(x=x, a=hash_a[1], b=hash_b[1]), 1, results, hash_fn_inds, x)
    results, hash_fn_inds = update_hashtable(hash_fn_partial(x=x, a=hash_a[2], b=hash_b[2]), 2, results, hash_fn_inds, x)
    results, hash_fn_inds = update_hashtable(hash_fn_partial(x=x, a=hash_a[3], b=hash_b[3]), 3, results, hash_fn_inds, x)
    results, hash_fn_inds = update_hashtable(hash_fn_partial(x=x, a=hash_a[4], b=hash_b[4]), 4, results, hash_fn_inds, x)

    total_word_count += 1

print("Done loop 1")

words = open('words_stream.txt', 'r')
counts = {}
errors = {}
for line in words:
    x = int(line.strip())
    lst_hashinds = hash_fn_inds[x]
    vals = []
    for fn_num in range(len(lst_hashinds)):
        ind = lst_hashinds[fn_num]
        vals.append(results[ind][fn_num])
    approx_count = min(vals)
    counts[x] = approx_count
    true_count = true_counts_dict[x]
    errors[x] = (abs(approx_count - true_count))/true_count

print("done loop 2")

error_plot = np.array([value for key, value in sorted(errors.items())])
true_freq = np.array([true_counts_dict[key]/total_word_count for key, _ in sorted(errors.items())])

import matplotlib.pyplot as plt

plt.scatter(true_freq, error_plot)

plt.xlabel("Exact Word Frequency")
plt.ylabel("Relative Error")
plt.title("Relative Error vs Exact Word Frequency")
plt.xscale('log')
plt.yscale('log')
plt.xticks([0.00000001, 0.0000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01,0.1, 1])
plt.yticks([10**-5, 10**-3, 10**-1, 10**0, 10**1, 10**3, 10**5, 10**7])

plt.savefig("relative_error_vs_exact_word_frequency.png")


import matplotlib.pyplot as plt

plt.scatter(true_freq, error_plot)
plt.axhline(y=1, color='r', linewidth=2)
plt.axvline(x=3*10**-8, color='r', linewidth=2)

plt.xlabel("Exact Word Frequency")
plt.ylabel("Relative Error")
plt.title("Relative Error vs Exact Word Frequency with Lines at Error=1")
plt.xscale('log')
plt.yscale('log')
plt.xticks([0.00000001, 0.0000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01,0.1, 1])
plt.yticks([10**-5, 10**-3, 10**-1, 10**0, 10**1, 10**3, 10**5, 10**7])

plt.savefig("relative_error_vs_exact_word_frequency_withlines.png")