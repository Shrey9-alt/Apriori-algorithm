import csv
import time
from itertools import combinations, chain
from collections import defaultdict

def find_frequent_1_itemsets(transactions, min_support):
    """Find frequent 1-itemsets."""
    item_count = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            item_count[frozenset([item])] += 1
    return {itemset for itemset, count in item_count.items() if count >= min_support}

def apriori_gen(frequent_itemsets, k):
    """Generate candidate itemsets of size k."""
    candidates = set()
    itemsets = list(frequent_itemsets)
    for i in range(len(itemsets)):
        for j in range(i + 1, len(itemsets)):
            l1, l2 = list(itemsets[i]), list(itemsets[j])
            if l1[:k - 2] == l2[:k - 2]:
                candidate = frozenset(itemsets[i] | itemsets[j])
                if not has_infrequent_subset(candidate, frequent_itemsets):
                    candidates.add(candidate)
    return candidates

def has_infrequent_subset(candidate, frequent_itemsets):
    """Check if a candidate has any infrequent subset."""
    for subset in combinations(candidate, len(candidate) - 1):
        if frozenset(subset) not in frequent_itemsets:
            return True
    return False

def apriori(transactions, min_support):
    """Apriori algorithm to find frequent itemsets."""
    start_time = time.time()
    L = []
    k = 1
    Lk = find_frequent_1_itemsets(transactions, min_support)
    
    while Lk:
        L.append(Lk)
        Ck = apriori_gen(Lk, k + 1)
        item_count = defaultdict(int)
        for transaction in transactions:
            for candidate in Ck:
                if candidate.issubset(transaction):
                    item_count[candidate] += 1
        Lk = {itemset for itemset, count in item_count.items() if count >= min_support}
        k += 1

    # Flatten the list of sets and format the output as required
    frequent_itemsets = set(chain.from_iterable(L))
    formatted_output = "".join(
        "{" + ",".join(map(str, sorted(itemset))) + "}" for itemset in frequent_itemsets
    )
    
    end_time = time.time()
    total_items = len(frequent_itemsets)
    total_time = end_time - start_time

    # Add summary information
    summary = f"\nEnd - total items: {total_items}\nTotal running time: {total_time:.6f}"
    return formatted_output + summary

def load_transactions(file):
    """Load transactions from uploaded CSV file."""
    transactions = []
    reader = csv.reader(file)
    for row in reader:
        transactions.append(set(map(int, row)))
    return transactions

