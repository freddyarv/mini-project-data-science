from flask import Flask, request, jsonify
import numpy as np
import joblib
import os
from datetime import datetime

app = Flask(__name__)

# Dummy model and scaler initialization
model_directory = os.path.dirname(os.path.realpath(__file__))
model_file_path = os.path.join(model_directory, '..', 'Model', 'model.pkl')
model = joblib.load(model_file_path)

# Dummy authentication token, replace with a more secure mechanism in a production environment
api_token = "admin123"

# Decorator function for authentication
def requires_auth(f):
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if token and token == f"Bearer {api_token}":
            return f(*args, **kwargs)
        else:
            return jsonify({'error': 'Unauthorized'}), 401

    return decorated

# Decorator function for authorization (dummy role-based authorization)
def requires_role(role):
    def decorator(f):
        def decorated(*args, **kwargs):
            # In a real application, you would have a more robust authorization mechanism
            user_role = request.headers.get('X-User-Role')

            if user_role and user_role == role:
                return f(*args, **kwargs)
            else:
                return jsonify({'error': 'Forbidden'}), 403

        return decorated

    return decorator

# Fungsi untuk mengonversi tanggal menjadi nilai numerik
def convert_date_to_numeric(date_value):
    # Jika tanggal dalam bentuk datetime, konversi ke timestamp UNIX
    if isinstance(date_value, datetime):
        timestamp = int(date_value.timestamp())
    else:
        # Jika tanggal dalam bentuk string, gunakan strptime
        date_object = datetime.strptime(date_value, "%Y-%m-%d %H:%M:%S.%f")
        timestamp = int(date_object.timestamp())

    return timestamp

# API endpoint for pricing recommendations
@app.route('/api/pricing', methods=['POST'])
@requires_auth
@requires_role('admin')  # Example: Only admin users can access this endpoint
def get_pricing_recommendation():
    try:
        # Retrieve data from the JSON request
        data = request.json

        # Convert date to numeric using the provided function
        for item in data:
            item['date'] = convert_date_to_numeric(item['date'])

        # Convert data to numpy array and perform scaling
        input_data = np.array([[int(row['productid']), int(row['date'])] for row in data])

        # Make predictions with the model
        predictions = model.predict(input_data)

        # Return the predictions
        results = [{'productid': int(data[i]['productid']), 'pricing_recommendation': predictions[i]} for i in range(len(data))]
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
