from flask import Flask, request, render_template
from apriori_2882543 import run_apriori  # Correct import
import os
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        min_support = request.form.get('min_support', type=int)  # Minimum support
        
        if file:
            try:
                # Save the file temporarily
                if not os.path.exists('uploads'):
                    os.makedirs('uploads')
                file_path = os.path.join('uploads', file.filename)
                file.save(file_path)

                # Run Apriori algorithm
                start_time = time.time()  # Start timer
                results = run_apriori(file_path, min_support)
                end_time = time.time()  # End timer

                # Calculate runtime
                total_runtime = round(end_time - start_time, 4)

                # Render result page
                return render_template(
                    'result.html',
                    results=results["maximal_itemsets"],
                    total_items=results["total_items"],
                    runtime=total_runtime,
                    file_name=file.filename,
                    support=min_support
                )
            except Exception as e:
                return f"An error occurred: {str(e)}", 500

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
