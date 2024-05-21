from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Load the data
data = pd.read_csv('computer_components.tsv', sep='\t')

# Ensure the price column is numerical
data['price'] = pd.to_numeric(data['price'], errors='coerce')

# Initialize the current indices for each component
current_indices = {component: 0 for component in ["CPU", "MB", "GPU", "GAB", "SSD", "RAM", "COOL", "PSU"]}

@app.route('/')
def index():
    components = ["CPU", "MB", "GPU", "GAB", "SSD", "RAM", "COOL", "PSU"]
    best_options = {}
    total_price = 0
    for component in components:
        filtered_data = data[data["part"] == component].sort_values(by='price')
        if not filtered_data.empty:
            current_index = current_indices[component]
            best_options[component] = filtered_data.iloc[current_index:current_index + 1].to_dict(orient='records')
            if best_options[component]:
                total_price += best_options[component][0]['price']
        else:
            best_options[component] = []
    return render_template('index.html', best_options=best_options, total_price=total_price, current_indices=current_indices)

@app.route('/update_index/<component>/<direction>')
def update_index(component, direction):
    if direction == 'next':
        current_indices[component] += 1
    elif direction == 'prev' and current_indices[component] > 0:
        current_indices[component] -= 1
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

