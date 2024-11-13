from flask import Flask, request, render_template
from apriori_2882543 import apriori, load_transactions
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        file = request.files['file']
        min_support = int(request.form['min_support'])

        if file:
            transactions = load_transactions(file)
            results = apriori(transactions, min_support)
            return render_template('result.html', results=results, support=min_support)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
