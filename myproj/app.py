from flask import Flask, request, render_template
from apriori_2882543 import apriori, load_transactions
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        min_support = int(request.form['min_support'])

      if file:
    # Load the transactions from the uploaded file
    transactions = load_transactions(file)
    # Run the Apriori algorithm
    results, runtime = apriori(transactions, min_support)
    return render_template('result.html', results=results, support=min_support, runtime=runtime)

    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
