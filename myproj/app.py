from flask import Flask, request, render_template
from apriori_2882543.py import apriori_2882543.py
import csv
import os

app = Flask(__name__)

# Function to load transactions from the uploaded file
def load_transactions(file):
    file.stream.seek(0)  # Ensure we're at the start of the file
    reader = csv.reader(file.stream.read().decode('utf-8').splitlines())  # Decode bytes to string
    transactions = [set(row) for row in reader]  # Convert each row to a set
    return transactions

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        file = request.files['file']
        min_support = int(request.form['min_support'])

        if file:
            # Load the transactions from the uploaded file
            transactions = load_transactions(file)
            
            # Run the Apriori algorithm
            frequent_itemsets = apriori_2882543.py (transactions, min_support)
            frequent_itemsets = sorted(frequent_itemsets, key=lambda x: (len(x), x))

            # Render the results in the result.html template
            return render_template(
                'result.html',
                results=[list(itemset) for itemset in frequent_itemsets],
                support=min_support
            )
    
    return render_template('index.html')

if __name__ == '__main__':
    # Ensure compatibility with Render by using the environment variable for PORT
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
