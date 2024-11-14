import csv
from itertools import combinations, chain
from collections import defaultdict
import time

def find_frequent_1_itemsets(transactions, min_support):
    """Find frequent 1-itemsets."""
    item_count = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            item_count[frozenset([item])] += 1
    return {itemset for itemset, count in item_count.items() if count >= min_support}

def apriori_gen(frequent_itemsets, k):
    """Generate candidate itemsets."""
    candidates = set()
    itemsets = list(frequent_itemsets)
    for i in range(len(itemsets)):
        for j in range(i + 1, len(itemsets)):
            l1, l2 = list(itemsets[i]), list(itemsets[j])
            if l1[:k - 2] == l2[:k - 2] and l1[k - 2] < l2[k - 2]:
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
    """Apriori algorithm implementation."""
    frequent_itemsets = []
    k = 1
    Lk = find_frequent_1_itemsets(transactions, min_support)
    while Lk:
        frequent_itemsets.append(Lk)
        Ck = apriori_gen(Lk, k + 1)
        item_count = defaultdict(int)
        for transaction in transactions:
            for candidate in Ck:
                if candidate.issubset(transaction):
                    item_count[candidate] += 1
        Lk = {itemset for itemset, count in item_count.items() if count >= min_support}
        k += 1
    return set(chain.from_iterable(frequent_itemsets))

def load_transactions(file):
    """Load transactions from the uploaded CSV file."""
    transactions = []
    reader = csv.reader(file)
    for row in reader:
        transactions.append(set(map(int, row)))
    return transactions

def run_apriori(file, min_support):
    """Run the Apriori algorithm and format the output."""
    transactions = load_transactions(file)
    start_time = time.time()
    results = apriori(transactions, min_support)
    end_time = time.time()

    # Formatting output
    output = []
    output.append("Data Mining Apriori Algorithm at Google App Engine")
    output.append(f"Input file: {file.name}")
    output.append(f"Minimal support: {min_support}\n")
    output.append(f"{results}")
    output.append(f"\nEnd - total items: {len(results)}")
    output.append(f"Total running time: {end_time - start_time:.6f}")
    return "\n".join(output)

# Example usage in your Flask app
if __name__ == "__main__":
    with open("1000-out1.csv", "r") as file:
        print(run_apriori(file, min_support=20))

