import csv
from itertools import combinations, chain
from collections import defaultdict

def find_frequent_1_itemsets(exchanges, min_support):
    """Find frequent 1-itemsets"""
    item_count = defaultdict(int)
    for transaction in exchanges:
        for item in transaction:
            item_count[frozenset([item])] += 1
    return {itemset for itemset, count in item_count.items() if count >= min_support}

def apriori_gen(oftensets, k):
    """Generate candidate itemsets"""
    candidates = set()
    itemsets = list(oftensets)
    for i in range(len(itemsets)):
        for j in range(i + 1, len(itemsets)):
            l1, l2 = list(itemsets[i]), list(itemsets[j])
            if l1[:k - 2] == l2[:k - 2] and l1[k - 2] < l2[k - 2]:
                candidate = frozenset(itemsets[i] | itemsets[j])
                if not has_infrequent_subset(candidate, oftensets):
                    candidates.add(candidate)
    return candidates

def has_infrequent_subset(candidate, oftensets):
    """Check if a candidate has any infrequent subset"""
    for subset in combinations(candidate, len(candidate) - 1):
        if frozenset(subset) not in oftensets:
            return True
    return False

def apriori(exchanges, min_support):
    """Apriori algorithm implementation"""
    L = []
    k = 1
    Lk = find_frequent_1_itemsets(exchanges, min_support)
    while Lk:
        L.append(Lk)
        Ck = apriori_gen(Lk, k + 1)
        item_count = defaultdict(int)
        for transaction in exchanges:
            Ct = {candidate for candidate in Ck if candidate.issubset(transaction)}
            for candidate in Ct:
                item_count[candidate] += 1
        Lk = {itemset for itemset, count in item_count.items() if count >= min_support}
        k += 1
    return set(chain.from_iterable(L))

def load_transactions(file):
    """Load transactions from uploaded CSV file"""
    exchanges = []
    reader = csv.reader(file)
    for row in reader:
        exchanges.append(set(map(int, row)))
    return exchanges
