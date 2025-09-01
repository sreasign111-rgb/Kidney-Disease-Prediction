# This script reads the CSV data, cleans it, trains a Random Forest model, and saves it.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier # Imported the Random Forest Classifier
import joblib
import os

def train_and_save_model(data_path, model_dir='model', model_filename='Kidney_Disease_Prediction_Model.pkl'):
    """
    Loads data, trains a Random Forest Classifier model, and saves it to a file.
    """
    print("Starting model training process...")
    
    # Create the model directory if it doesn't exist
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        print(f"Created directory: {model_dir}")

    try:
        # Load the dataset
        df = pd.read_csv(data_path)
        print(f"Data loaded successfully from {data_path}.")

        # Data Cleaning and Preprocessing
        # First, drop the 'id' column as it's not a feature for prediction
        df = df.drop('id', axis=1)
        
        # Replace '?' values with NaN for proper handling
        df = df.replace('?', pd.NA)

        # Drop rows with any missing values. For a real-world project,
        # you might use more advanced imputation methods.
        df = df.dropna()
        
        # Manually encode categorical features to numerical values
        df['rbc'] = df['rbc'].map({'normal': 1, 'abnormal': 0})
        df['pc'] = df['pc'].map({'normal': 1, 'abnormal': 0})
        df['pcc'] = df['pcc'].map({'present': 1, 'notpresent': 0})
        df['ba'] = df['ba'].map({'present': 1, 'notpresent': 0})
        df['htn'] = df['htn'].map({'yes': 1, 'no': 0})
        df['dm'] = df['dm'].map({'yes': 1, 'no': 0})
        df['cad'] = df['cad'].map({'yes': 1, 'no': 0})
        df['appet'] = df['appet'].map({'good': 1, 'poor': 0})
        df['pe'] = df['pe'].map({'yes': 1, 'no': 0})
        df['ane'] = df['ane'].map({'yes': 1, 'no': 0})

        # The target column is 'classification'. Map its values to 1 and 0.
        df['classification'] = df['classification'].map({'ckd': 1, 'notckd': 0})

        # Define features (X) and target (y)
        X = df.drop('classification', axis=1)
        y = df['classification']

        # Split data for training and testing
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize and train the Random Forest Classifier
        # You can tune the n_estimators and other hyperparameters for better performance
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        print("Random Forest model trained successfully.")

        # Save the trained model to a pickle file inside the 'model' directory
        model_path = os.path.join(model_dir, model_filename)
        joblib.dump(model, model_path)
        print(f"Model saved as '{model_path}'.")

    except FileNotFoundError:
        print(f"Error: The file '{data_path}' was not found. Please make sure the CSV file is in the '{os.path.dirname(data_path)}' directory.")
    except Exception as e:
        print(f"An unexpected error occurred during training: {e}")

if __name__ == '__main__':
    train_and_save_model('data/kidney_disease_data.csv')
