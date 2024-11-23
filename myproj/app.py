from flask import Flask, request, render_template
from apriori_2882543 import apriori, load_transactions
import os
from io import TextIOWrapper
import csv

app = Flask(__name__)

def load_transactions_from_filestorage(file_storage):
    """Helper function to load transactions directly from FileStorage."""
    transactions = []
    file = TextIOWrapper(file_storage, encoding='utf-8')  # Convert FileStorage to a readable object
    reader = csv.reader(file)
    for row in reader:
        transactions.append(set(row))
    file.close()
    return transactions

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        file = request.files['file']
        min_support = int(request.form['min_support'])

        if file:
            try:
                # Load the transactions from the uploaded file
                transactions = load_transactions_from_filestorage(file)
                # Run the Apriori algorithm
                results = apriori(transactions, min_support)
                return render_template('result.html', results=results, support=min_support)
            except Exception as e:
                return f"An error occurred: {str(e)}", 500

    # Render the upload form
    return render_template('index.html')

if __name__ == '__main__':
    # Ensure compatibility with Render by using the environment variable for PORT
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
