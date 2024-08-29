import pandas as pd
import numpy as np
import re
import spacy
import matplotlib.pyplot as plt
import seaborn as sns
import io
from flask import Flask, request, jsonify, render_template, send_file
from PyPDF2 import PdfReader
from collections import Counter

app = Flask(__name__)

nlp = spacy.load("en_core_web_sm")

df = pd.read_csv('CarPrice.csv')

def preprocess_data():
    """Preprocess data for statistics and unique values."""
    df.drop(columns=["car_ID"], inplace=True)
    description = df.describe(include='object')
    car_names = df['CarName'].unique()
    fuel_types = df['fueltype'].unique()
    car_bodies = df['carbody'].unique()
    drive_wheels = df['drivewheel'].unique()
    engine_locations = df['enginelocation'].unique()
    return description, car_names, fuel_types, car_bodies, drive_wheels, engine_locations

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_customer_requirements(text):
    """Extract customer requirements from the text."""
    doc = nlp(text)
    requirements = {
        "car_type": None,
        "fuel_type": None,
        "color": None,
        "distance_travelled": None,
        "make_year": None,
        "transmission_type": None
    }

    car_types = ["hatchback", "suv", "sedan"]
    fuel_types = ["petrol", "diesel", "electric", "hybrid"]
    transmissions = ["manual", "automatic"]

    for token in doc:
        if token.text.lower() in car_types:
            requirements["car_type"] = token.text
        elif token.text.lower() in fuel_types:
            requirements["fuel_type"] = token.text
        elif token.like_num and "km" in token.head.text.lower():
            requirements["distance_travelled"] = token.text + " km"
        elif token.text.isdigit() and 1990 < int(token.text) < 2025:
            requirements["make_year"] = token.text
        elif token.text.lower() in transmissions:
            requirements["transmission_type"] = token.text

    color_pattern = r'\b(?:red|blue|green|black|white|silver|grey|yellow|orange|brown)\b'
    match = re.search(color_pattern, text, re.IGNORECASE)
    if match:
        requirements["color"] = match.group(0)

    return requirements

def extract_company_policies(text):
    """Extract company policies from the text."""
    policies = {
        "free_rc_transfer": "Free RC Transfer" in text,
        "money_back_guarantee": "5-Day Money Back Guarantee" in text,
        "free_rsa": "Free RSA for One Year" in text,
        "return_policy": "Return Policy" in text
    }
    return policies

def extract_customer_objections(text):
    """Extract customer objections from the text."""
    objections = {
        "refurbishment_quality": "refurbishment quality" in text.lower(),
        "car_issues": "car issues" in text.lower(),
        "price_issues": "price" in text.lower(),
        "experience_issues": any(word in text.lower() for word in ["customer experience", "wait time", "salesperson behavior"])
    }
    return objections

def calculate_accuracy(data):
    """Calculate accuracy of extracted information."""
    correct = sum(value is not None for value in data.values())
    total = len(data)
    accuracy = (correct / total) * 100 if total > 0 else 0
    return round(accuracy, 2)

def visualize_most_requested_cars():
    """Visualize the distribution of most requested cars."""
    most_requested = df['CarName'].value_counts().head(10)  # Top 10 most requested cars
    plt.figure(figsize=(12, 6))
    sns.barplot(x=most_requested.index, y=most_requested.values, palette='viridis')
    plt.xticks(rotation=45)
    plt.xlabel('Car Names')
    plt.ylabel('Frequency')
    plt.title('Most Requested Cars')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

def visualize_price_ranges():
    """Visualize popular price ranges."""
    plt.figure(figsize=(10, 6))
    sns.histplot(df['price'], bins=20, color='green')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.title('Popular Price Ranges')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

def visualize_preferred_car_types():
    """Visualize preferred car types."""
    preferred_car_types = df['carbody'].value_counts()
    plt.figure(figsize=(8, 6))
    sns.barplot(x=preferred_car_types.index, y=preferred_car_types.values, palette='coolwarm')
    plt.xlabel('Car Types')
    plt.ylabel('Frequency')
    plt.title('Preferred Car Types')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

def visualize_common_objections():
    """Visualize frequently raised objections."""
    objection_counts = Counter(['refurbishment_quality', 'car_issues', 'price_issues', 'experience_issues'])
    objection_df = pd.DataFrame.from_dict(objection_counts, orient='index').reset_index()
    objection_df.columns = ['Objection', 'Frequency']
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Objection', y='Frequency', data=objection_df, palette='autumn')
    plt.xlabel('Objections')
    plt.ylabel('Frequency')
    plt.title('Frequently Raised Objections')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

@app.route('/compare', methods=['POST'])
def compare_data():
    user_data = request.json.get('user_data', {})
    if not user_data:
        return jsonify({"error": "No user data provided"}), 400

    user_df = pd.DataFrame([user_data])
    user_df['price'] = np.nan

    plt.figure(figsize=(10, 6))
    sns.histplot(user_df['price'], bins=20, color='blue', label='User Data')
    sns.histplot(df['price'], bins=20, color='orange', label='Dataset')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.title('Price Distribution Comparison')
    plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return send_file(buf, mimetype='image/png')

def process_transcript(text):
    """Process the transcript to extract information and calculate accuracy."""
    customer_requirements = extract_customer_requirements(text)
    company_policies = extract_company_policies(text)
    customer_objections = extract_customer_objections(text)

    accuracy = calculate_accuracy(customer_requirements)

    result = {
        "customer_requirements": customer_requirements,
        "company_policies": company_policies,
        "customer_objections": customer_objections,
        "accuracy": accuracy
    }
    return result

@app.route('/visualize', methods=['GET'])
def visualize_data():
    """Generate and return visualizations as PNG image."""
    buf = io.BytesIO()

    # Filter out only numeric columns for correlation heatmap
    numeric_df = df.select_dtypes(include=[np.number])
    
    # Correlation Heatmap
    plt.figure(figsize=(15, 10))
    if not numeric_df.empty:
        corr = numeric_df.corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Heatmap')
    else:
        plt.text(0.5, 0.5, 'No numeric data available', horizontalalignment='center', verticalalignment='center')
    
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Additional visualizations if needed (e.g., distribution of car prices)

    return send_file(buf, mimetype='image/png')

@app.route('/most-requested-cars', methods=['GET'])
def show_most_requested_cars():
    """Endpoint to show most requested cars."""
    buf = visualize_most_requested_cars()
    return send_file(buf, mimetype='image/png')

@app.route('/price-ranges', methods=['GET'])
def show_price_ranges():
    """Endpoint to show popular price ranges."""
    buf = visualize_price_ranges()
    return send_file(buf, mimetype='image/png')

@app.route('/preferred-car-types', methods=['GET'])
def show_preferred_car_types():
    """Endpoint to show preferred car types."""
    buf = visualize_preferred_car_types()
    return send_file(buf, mimetype='image/png')

@app.route('/common-objections', methods=['GET'])
def show_common_objections():
    """Endpoint to show frequently raised objections."""
    buf = visualize_common_objections()
    return send_file(buf, mimetype='image/png')

@app.route('/statistics', methods=['GET'])
def show_statistics():
    """Provide data statistics and unique values as JSON."""
    description, car_names, fuel_types, car_bodies, drive_wheels, engine_locations = preprocess_data()
    return jsonify({
        "description": description.to_dict(),
        "car_names": car_names.tolist(),
        "fuel_types": fuel_types.tolist(),
        "car_bodies": car_bodies.tolist(),
        "drive_wheels": drive_wheels.tolist(),
        "engine_locations": engine_locations.tolist()
    })

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """Handle file upload and process transcript."""
    if request.method == 'POST':
        file = request.files['file']
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(file)
        else:
            text = file.read().decode('utf-8')

        extracted_info = process_transcript(text)
        return jsonify({"extracted_info": extracted_info})

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
