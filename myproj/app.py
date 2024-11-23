from flask import Flask, request, render_template
from apriori_2882543 import apriori
import os
from io import TextIOWrapper
import csv
import time

app = Flask(__name__)

def load_transactions_from_filestorage(file_storage):
    """Helper function to load transactions directly from FileStorage."""
    transactions = []
    try:
        file = TextIOWrapper(file_storage.stream, encoding='utf-8')  # Convert FileStorage to a readable object
        reader = csv.reader(file)
        for row in reader:
            transactions.append(set(row))  # Convert rows to sets for Apriori
        file.close()
    except Exception as e:
        raise ValueError(f"Error while parsing the uploaded file: {e}")
    return transactions

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        file = request.files['file']
        min_support = request.form.get('min_support', type=int)  # Convert min_support to int

        if file:
            try:
                # Load transactions from the uploaded file
                transactions = load_transactions_from_filestorage(file)

                # Run the Apriori algorithm
                start_time = time.time()  # Start timer
                results = apriori(transactions, min_support)
                end_time = time.time()  # End timer

                # Calculate runtime
                total_runtime = round(end_time - start_time, 4)

                # Render the result page
                return render_template(
                    'result.html',
                    results=results,
                    support=min_support,
                    file_name=file.filename,
                    total_items=len(results),
                    runtime=total_runtime
                )
            except ValueError as ve:
                return f"An error occurred while processing the file: {str(ve)}", 400
            except Exception as e:
                return f"An unexpected error occurred: {str(e)}", 500

    # Render the upload form
    return render_template('index.html')

if __name__ == '__main__':
    # Ensure compatibility with Render by using the environment variable for PORT
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
