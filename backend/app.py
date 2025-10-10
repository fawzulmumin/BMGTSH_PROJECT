from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import joblib
import pandas as pd
import os
import logging
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import numpy as np

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), '../frontend'),
            static_folder=os.path.join(os.path.dirname(__file__), '../frontend'))

# Initialize CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Load the model, scaler, encoder, and feature names
model = joblib.load(os.path.join(os.path.dirname(__file__), 'best_model.pkl'))
sc_y = joblib.load(os.path.join(os.path.dirname(__file__), 'scaler_y.pkl'))
sc_X = joblib.load(os.path.join(os.path.dirname(__file__), 'scaler_X.pkl'))
ohe = joblib.load(os.path.join(os.path.dirname(__file__), 'ohe_encoder.pkl'))
feature_names = joblib.load(os.path.join(os.path.dirname(__file__), 'feature_names.pkl'))

# Load dataset for visualization purposes
data = pd.read_csv('dataset.csv')

# Process the data for correlation matrix and feature encoding
df = data.copy()
string_feat = ['Provinsi']
data_ohe_res = pd.DataFrame(ohe.transform(df[string_feat]).toarray(), columns=ohe.get_feature_names_out())
df = pd.concat([df, data_ohe_res], axis=1)
df = df.drop(columns=string_feat)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        app.logger.debug(f"Received data: {data}")

        # Ensure all required fields are present
        required_fields = ['Provinsi', 'Tahun', 'Luas_Panen', 'Curah_hujan', 'Kelembapan', 'Suhu_rata_rata']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing field: {field}")

        # Prepare the input data
        provinsi = data['Provinsi']
        tahun = int(data['Tahun'])
        luas_panen = float(data['Luas_Panen'])
        curah_hujan = float(data['Curah_hujan'])
        kelembapan = float(data['Kelembapan'])
        suhu_rata_rata = float(data['Suhu_rata_rata'])

        # Create DataFrame
        input_data = pd.DataFrame([[provinsi, tahun, luas_panen, curah_hujan, kelembapan, suhu_rata_rata]],
                                  columns=['Provinsi', 'Tahun', 'Luas Panen', 'Curah hujan', 'Kelembapan', 'Suhu rata-rata'])
        app.logger.debug(f"Prepared input_data: {input_data}")

        # Feature Encoding
        input_data_ohe = ohe.transform(input_data[['Provinsi']]).toarray()
        input_data_ohe_df = pd.DataFrame(input_data_ohe, columns=ohe.get_feature_names_out())
        input_data = pd.concat([input_data[['Luas Panen', 'Curah hujan', 'Kelembapan', 'Suhu rata-rata']], input_data_ohe_df], axis=1)
        app.logger.debug(f"Encoded input_data: {input_data}")

        # Ensure input data has the same features as used in training
        input_data = input_data.reindex(columns=feature_names, fill_value=0)
        app.logger.debug(f"Reindexed input_data: {input_data}")

        # Feature Scaling
        input_data_scaled = sc_X.transform(input_data)
        app.logger.debug(f"Scaled input_data: {input_data_scaled}")

        # Prediction
        prediction_scaled = model.predict(input_data_scaled)
        prediction = sc_y.inverse_transform(prediction_scaled.reshape(-1, 1))
        app.logger.debug(f"Prediction: {prediction}")

        # Format prediction
        formatted_prediction = f"{prediction[0][0]:,.2f}"

        return jsonify({'prediction': formatted_prediction})
    except Exception as e:
        app.logger.error(f"Error during prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/visualization_data', methods=['GET'])
def get_visualization_data():
    try:
        # Data for bar chart (average production by province)
        avg_production_by_province = data.groupby('Provinsi')['Produksi'].mean().reset_index()
        bar_chart_data = {
            'labels': avg_production_by_province['Provinsi'].tolist(),
            'data': avg_production_by_province['Produksi'].tolist()
        }

        # Data for line chart (average production by year)
        avg_production_by_year = data.groupby('Tahun')['Produksi'].mean().reset_index()
        line_chart_data = {
            'labels': avg_production_by_year['Tahun'].tolist(),
            'data': avg_production_by_year['Produksi'].tolist()
        }

        # Data for correlation matrix
        correlation_matrix = df.loc[:, 'Luas Panen':'Suhu rata-rata'].corr()
        correlation_matrix_data = {
            'labels': correlation_matrix.columns.tolist(),
            'data': correlation_matrix.values.tolist()
        }

        return jsonify({
            'barChart': bar_chart_data,
            'lineChart': line_chart_data,
            'correlationMatrix': correlation_matrix_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/script.js')
def serve_js():
    return send_from_directory(app.static_folder, 'script.js')

@app.route('/style.css')
def serve_css():
    return send_from_directory(app.static_folder, 'style.css')

if __name__ == '__main__':
    app.run(debug=True)
