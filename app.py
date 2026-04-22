from flask import Flask, render_template, request
import mysql.connector
import matplotlib.pyplot as plt
import os
from sklearn.linear_model import LogisticRegression
import numpy as np



app = Flask(__name__)

# DB Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pass@123",
    database="household_finance"
)
cursor = conn.cursor()

@app.route('/')
def home():
    return render_template('index.html')

# ✅ FAMILY PAGE ROUTE
@app.route('/family', methods=['POST'])
def family():
    family_size = int(request.form['family_size'])
    return render_template('family.html', family_size=family_size)

# (optional old route)
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    family_size = request.form['family_size']

    query = "INSERT INTO users (name, family_size) VALUES (%s, %s)"
    cursor.execute(query, (name, family_size))
    conn.commit()

    return "Data Saved Successfully!"

@app.route('/save_family', methods=['POST'])
def save_family():
    family_size = int(request.form['family_size'])

    total_income = 0

    for i in range(family_size):
        income = float(request.form[f'income{i}'])
        total_income += income

    # 👉 Go to expenses page
    return render_template('expenses.html', total_income=total_income)


# 🔥 FIRST: Helper Functions (NO @app.route here)

def classify_risk(savings_percent):
    if savings_percent > 20:
        return "Safe"
    elif savings_percent > 10:
        return "Moderate"
    else:
        return "Risky"


def generate_suggestions(grocery, mobile, other):
    suggestions = []

    if grocery > 5000:
        suggestions.append("Reduce grocery expenses")

    if mobile > 1000:
        suggestions.append("Choose a cheaper mobile plan")

    if other > 3000:
        suggestions.append("Control unnecessary expenses")

    if len(suggestions) == 0:
        suggestions.append("Your spending is well managed!")

    return suggestions


def train_model():
    # sample training data
    X = np.array([[10], [15], [25], [30], [5], [8]])
    y = np.array([0, 1, 2, 2, 0, 0])  
    # 0 = Risky, 1 = Moderate, 2 = Safe

    model = LogisticRegression()
    model.fit(X, y)
    return model

model = train_model()


# 🔥 NOW: Route function
@app.route('/result', methods=['POST'])
def result():
    total_income = float(request.form['total_income'])

    grocery = float(request.form['grocery'])
    education = float(request.form['education'])
    electricity = float(request.form['electricity'])
    gas = float(request.form['gas'])
    medical = float(request.form['medical'])
    rent = float(request.form['rent'])
    mobile = float(request.form['mobile'])
    tv = float(request.form['tv'])
    other = float(request.form['other'])

    total_expense = (grocery + education + electricity + gas +
                     medical + rent + mobile + tv + other)

    savings = total_income - total_expense
    savings_percent = (savings / total_income) * 100

    # ✅ ML Prediction
    prediction = model.predict([[savings_percent]])[0]

    if prediction == 0:
        risk = "Risky"
    elif prediction == 1:
        risk = "Moderate"
    else:
        risk = "Safe"

    # ✅ Suggestions
    suggestions = generate_suggestions(grocery, mobile, other)

    # ✅ GRAPH CODE (PUT HERE 🔥)
    categories = ['Grocery', 'Education', 'Electricity', 'Gas', 'Medical', 'Rent', 'Mobile', 'TV', 'Other']
    values = [grocery, education, electricity, gas, medical, rent, mobile, tv, other]

    plt.figure(figsize=(6,6))

    categories = ['Grocery', 'Education', 'Electricity', 'Gas', 'Medical', 'Rent', 'Mobile', 'TV', 'Other']
    values = [grocery, education, electricity, gas, medical, rent, mobile, tv, other]

     # Remove zero values
    filtered_categories = []
    filtered_values = []

    for i in range(len(values)):
        if values[i] > 0:
            filtered_categories.append(categories[i])
            filtered_values.append(values[i])

    plt.figure(figsize=(6,6))
    plt.pie(
        values,
        labels=categories,
        autopct='%1.1f%%',
        startangle=140
    )
    plt.tight_layout()

    plt.title("Expense Distribution")
    plt.tight_layout()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    graph_path = os.path.join(base_dir, 'static', 'graph.png')
    plt.savefig(graph_path)
    plt.close()

    # ✅ Return result
    return render_template('result.html',
                           income=total_income,
                           expense=total_expense,
                           savings=savings,
                           percent=savings_percent,
                           risk=risk,
                           suggestions=suggestions,
                           graph='graph.png')



if __name__ == '__main__':
    app.run(debug=True)    

 



"""@app.route('/result', methods=['POST'])
    
def classify_risk(savings_percent):
    if savings_percent > 20:
        return "Safe"
    elif savings_percent > 10:
        return "Moderate"
    else:
        return "Risky"
def result():
    total_income = float(request.form['total_income'])

    grocery = float(request.form['grocery'])
    education = float(request.form['education'])
    electricity = float(request.form['electricity'])
    gas = float(request.form['gas'])
    medical = float(request.form['medical'])
    rent = float(request.form['rent'])
    mobile = float(request.form['mobile'])
    tv = float(request.form['tv'])
    other = float(request.form['other'])

    total_expense = (grocery + education + electricity + gas +
                     medical + rent + mobile + tv + other)

    savings = total_income - total_expense
    savings_percent = (savings / total_income) * 100

    # 🔥 NEW FEATURES
    risk = classify_risk(savings_percent)
    suggestions = generate_suggestions(grocery, mobile, other)

    return render_template('result.html',
                           income=total_income,
                           expense=total_expense,
                           savings=savings,
                           percent=savings_percent,
                           risk=risk,
                           suggestions=suggestions)

def generate_suggestions(grocery, mobile, other):
    suggestions = []

    if grocery > 5000:
        suggestions.append("Reduce grocery expenses")

    if mobile > 1000:
        suggestions.append("Choose a cheaper mobile plan")

    if other > 3000:
        suggestions.append("Control unnecessary expenses")

    if len(suggestions) == 0:
        suggestions.append("Your spending is well managed!")

    return suggestions

# ✅ ALWAYS KEEP THIS LAST
if __name__ == '__main__':
    app.run(debug=True)"""