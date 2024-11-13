from flask import Flask, request, render_template
from apriori_2882543 import apriori
import csv
import os

app = Flask(__name__)

def load_transactions(file):
    # Open the uploaded file in text mode
    file.stream.seek(0)  # Ensure we're at the start of the file
    reader = csv.reader(file.stream.read().decode('utf-8').splitlines())  # Decode bytes to string
    transactions = [row for row in reader]
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
            results = apriori(transactions, min_support)
            return render_template('result.html', results=results, support=min_support)
    
    return render_template('index.html')

if __name__ == '__main__':
    # Ensure compatibility with Render by using the environment variable for PORT
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

