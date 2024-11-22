import csv
import time
from collections import defaultdict, Counter
from itertools import combinations, chain

def load_transactions(uploaded_file):
    """Load transactions from an uploaded CSV file"""
    transactions = []
    uploaded_file.stream.seek(0)  # Ensure we're at the start of the file
    reader = csv.reader(uploaded_file.stream.read().decode('utf-8').splitlines())  # Decode and split lines
    for row in reader:
        transactions.append(set(row))
    return transactions

def find_frequent_1_itemsets(transactions, min_support):
    """Find frequent 1-itemsets"""
    item_count = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            item_count[frozenset([item])] += 1
    return {itemset for itemset, count in item_count.items() if count >= min_support}

def apriori_gen(itemsets, k):
    """Generate candidate itemsets"""
    candidates = set()
    itemsets = list(itemsets)
    for i in range(len(itemsets)):
        for j in range(i + 1, len(itemsets)):
            l1, l2 = list(itemsets[i]), list(itemsets[j])
            if l1[:k - 2] == l2[:k - 2] and l1[k - 2] < l2[k - 2]:
                candidate = frozenset(itemsets[i] | itemsets[j])
                if not has_infrequent_subset(candidate, itemsets):
                    candidates.add(candidate)
    return candidates

def has_infrequent_subset(candidate, itemsets):
    """Check if a candidate has any infrequent subset"""
    for subset in combinations(candidate, len(candidate) - 1):
        if frozenset(subset) not in itemsets:
            return True
    return False

def apriori(transactions, min_support):
    """Apriori algorithm implementation"""
    L = []
    k = 1
    Lk = find_frequent_1_itemsets(transactions, min_support)
    while Lk:
        L.append(Lk)
        Ck = apriori_gen(Lk, k + 1)
        item_count = defaultdict(int)
        for transaction in transactions:
            Ct = {candidate for candidate in Ck if candidate.issubset(transaction)}
            for candidate in Ct:
                item_count[candidate] += 1
        Lk = {itemset for itemset, count in item_count.items() if count >= min_support}
        k += 1
    return set(chain.from_iterable(L))

def get_maximal_frequent_itemsets(frequent_itemsets):
    """Extract maximal frequent itemsets from all frequent itemsets"""
    maximal = []
    for itemset in sorted(frequent_itemsets, key=len, reverse=True):
        if not any(set(itemset).issubset(set(max_itemset)) for max_itemset in maximal):
            maximal.append(itemset)
    return maximal

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Apriori Algorithm Implementation')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file')
    parser.add_argument('-m', '--min_support', type=int, required=True, help='Minimum support value')
    args = parser.parse_args()

    start_time = time.time()
    transactions = load_transactions(args.input)
    min_support = args.min_support

    # Run Apriori Algorithm
    frequent_itemsets = apriori(transactions, min_support)

    # Extract Maximal Frequent Itemsets
    maximal_frequent_itemsets = get_maximal_frequent_itemsets(frequent_itemsets)
    maximal_frequent_itemsets = sorted(maximal_frequent_itemsets, key=lambda x: (len(x), x))

    print(f"Input file: {args.input}")
    print(f"Minimal support: {min_support}")
    print("{", end="")
    formatted_itemsets = [f"{{{','.join(map(str, itemset))}}}" for itemset in maximal_frequent_itemsets]
    print(",".join(formatted_itemsets), end="")
    print("}")
    print(f"\nEnd - total items: {len(maximal_frequent_itemsets)}")
    print(f"Total running time: {time.time() - start_time:.6f} seconds")
