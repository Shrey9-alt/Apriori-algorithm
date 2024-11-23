from flask import Flask, request, render_template
from apriori_2882543 import apriori, load_transactions
import os
import time  # For tracking runtime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        file = request.files['file']
        min_support = int(request.form['min_support'])

        if file:
            # Load the transactions from the uploaded file
            transactions = load_transactions(file)

            # Start timing the Apriori algorithm
            start_time = time.time()
            results = apriori(transactions, min_support)
            end_time = time.time()
            
            # Calculate total runtime
            total_time = end_time - start_time

            # Pass all data to the result template
            return render_template(
                'result.html',
                results=results,
                support=min_support,
                file_name=file.filename,
                total_items=len(results),
                runtime=total_time
            )

    # Render the upload form
    return render_template('index.html')

if __name__ == '__main__':
    # Ensure compatibility with Render by using the environment variable for PORT
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
