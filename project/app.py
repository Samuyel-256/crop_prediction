from flask import Flask, request, render_template, session
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pandas as pd

app = Flask(__name__)
app.secret_key = 'SA MUYEL'  # replace with your secret keyddddd;;, dnjkhkdxwgkkusuhdohuh 

# Read data
data = pd.read_csv('Crop_recommendation.csv')

# Split data into features (X) and target variable (y)
X = data.drop('label', axis=1)
y = data['label']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
classifier = DecisionTreeClassifier(criterion='entropy', random_state=42)
classifier.fit(X_train, y_train)

@app.route('/')
def home():
    return render_template('index.html', outputs=session.get('outputs', []))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predictor', methods=['POST'])
def predictor():
    if request.method == 'POST':
        # Get user input
        Phosphorus = request.form['phosphorus']
        potassium = request.form['potassium']
        nitrogen = request.form['nitrogen']
        rainfall = request.form['rainfall']
        humidity = request.form['humidity']
        temperature = request.form['temperature']
        ph = request.form['ph']

        # Check if input fields are empty and provide a default value
        default_value = 0.0  # Replace with a suitable default value for your application
        Phosphorus = default_value if Phosphorus == '' else float(Phosphorus)
        potassium = default_value if potassium == '' else float(potassium)
        nitrogen = default_value if nitrogen == '' else float(nitrogen)
        rainfall = default_value if rainfall == '' else float(rainfall)
        humidity = default_value if humidity == '' else float(humidity)
        temperature = default_value if temperature == '' else float(temperature)
        ph = default_value if ph == '' else float(ph)

        # Make prediction
        predicted_crop = classifier.predict([[Phosphorus, potassium, nitrogen, rainfall, humidity, temperature, ph]])[0]

        # Render result template with prediction
        return render_template('result.html', predicted_crop=predicted_crop)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Send email (replace this with your email sending logic)
        # For demonstration purposes, we'll print the data here
        print(f"Name: {name}\nEmail: {email}\nMessage: {message}")

        # Redirect to a thank you page or homepage
        return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
