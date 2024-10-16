import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import joblib
import json

class PriceModel:
    def __init__(self, data=None):
        self.data = data
        self.features_to_standardize = ['size', 'dorms', 'toilets', 'garage']
        self.locations = [col for col in data.columns if col.startswith('location_')] if data is not None else None
        self.layers = [
            ('relu', 64),
            ('relu', 32),
            ('tanh', 18),
            (None, 1)
        ]
        self.batch_size = 8
        self.max_epochs = 100
        self.test_size = 0.2
        self.valid_size = 0.2
        self.scaler = StandardScaler()
        self.early_stopping = tf.keras.callbacks.EarlyStopping(patience=2)
        self.model = self.build_model() if data is not None else None

    def preprocess_data(self):
        # Preprocessing: Standardize the selected features
        self.data[self.features_to_standardize] = self.scaler.fit_transform(self.data[self.features_to_standardize])

        # Split the dataset
        X = self.data.drop(columns=['price'])
        y = self.data['price']
        self.X_train_val, self.X_test, self.y_train_val, self.y_test = train_test_split(X, y, test_size=self.test_size,
                                                                                        random_state=42)
        self.X_train, self.X_valid, self.y_train, self.y_valid = train_test_split(self.X_train_val, self.y_train_val,
                                                                                  test_size=self.valid_size,
                                                                                  random_state=42)

    def build_model(self):
        # Build a Sequential neural network model
        ann = tf.keras.models.Sequential()
        for layer in self.layers:
            ann.add(tf.keras.layers.Dense(units=layer[1], activation=layer[0]))
        ann.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_squared_error'])
        return ann

    def train(self):
        # Train the model
        self.model.fit(
            self.X_train,
            self.y_train,
            epochs=self.max_epochs,
            batch_size=self.batch_size,
            callbacks=[self.early_stopping],
            verbose=0,
            validation_data=(self.X_valid, self.y_valid)
        )

    def evaluate(self):
        # Evaluate the model
        test_loss, test_mse = self.model.evaluate(self.X_test, self.y_test)
        print(f"Test Loss: {test_loss}, Test MSE: {test_mse}")
        return test_loss, test_mse

    def predict(self, input_data):
        # Process custom input and make a prediction
        input_df = pd.DataFrame([input_data])
        input_df.drop(columns=['location'], inplace=True)

        # Add one-hot encoded location columns
        for loc in self.locations:
            input_df[loc] = 0
        input_df[self.locations[input_data['location']]] = 1

        # Standardize features using the same scaler
        input_df[self.features_to_standardize] = self.scaler.transform(input_df[self.features_to_standardize])

        prediction = self.model.predict(input_df)
        return np.exp(prediction[0][0])

    def plot_predictions(self):
        # Predict on the test set
        y_pred = self.model.predict(self.X_test)

        plt.figure(figsize=(9, 8))
        plt.scatter(self.y_test, y_pred, alpha=0.7, label='Predicted vs Actual')

        # Adding a regression line (fit line)
        m, b = np.polyfit(self.y_test, y_pred.ravel(), 1)  # Linear fit
        plt.plot(self.y_test, m * self.y_test + b, color='green', label=f"Predictions Fit", linestyle='--')

        # Plot the ideal fit line
        plt.plot([self.y_test.min(), self.y_test.max()], [self.y_test.min(), self.y_test.max()], '--', color='red',
                 label='Ideal Fit')

        plt.xlabel("Actual Prices")
        plt.ylabel("Predicted Prices")
        plt.title(f"Model Predictions vs Actual Prices")
        plt.legend()
        plt.show()

    def save_model(self, model_path='model.h5', scaler_path='scaler.pkl', config_path='config.json'):
        # Save the model to a file
        self.model.save(model_path)
        print(f"Model saved to {model_path}")

        # Save the scaler
        joblib.dump(self.scaler, scaler_path)
        print(f"Scaler saved to {scaler_path}")

        # Save the locations and other configs
        config = {
            'locations': self.locations
        }
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file)
        print(f"Configuration (locations) saved to {config_path}")

    @classmethod
    def load_model(cls, model_path='model.h5', scaler_path='scaler.pkl', config_path='config.json'):
        # Load the saved model
        model = tf.keras.models.load_model(model_path)
        print(f"Model loaded from {model_path}")

        # Load the saved scaler
        scaler = joblib.load(scaler_path)
        print(f"Scaler loaded from {scaler_path}")

        # Load the locations and other configs
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)

        locations = config['locations']
        print(f"Configuration (locations) loaded from {config_path}")

        # Create an instance of the class
        price_model = cls()
        price_model.model = model
        price_model.scaler = scaler
        price_model.locations = locations
        return price_model