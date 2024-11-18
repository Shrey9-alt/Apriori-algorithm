import csv
from itertools import combinations, chain
from collections import defaultdict
import time

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

def format_itemsets(itemsets):
    """Format the frequent itemsets to match the required output style"""
    formatted = "{{" + "}{".join([",".join(map(str, sorted(itemset))) for itemset in itemsets]) + "}}"
    return formatted

def run_apriori(file, min_support):
    """Run the Apriori algorithm and format the output"""
    exchanges = load_transactions(file)
    
    # Start timing the execution
    start_time = time.time()
    results = apriori(exchanges, min_support)
    end_time = time.time()
    
    # Formatting the output
    formatted_results = format_itemsets(results)
    
    output = []
    output.append(f"Minimal Support: {min_support}")
    output.append("\nFrequent Itemsets:\n")
    output.append(formatted_results)
    output.append(f"\n\nEnd - total items: {len(results)}")
    output.append(f"Total running time: {end_time - start_time:.6f} seconds")
    
    return "\n".join(output)

if __name__ == "__main__":
    # Replace with file handling for web applications
    with open('1000-out1.csv', 'r') as file:
        min_support = 20
        print(run_apriori(file, min_support))


