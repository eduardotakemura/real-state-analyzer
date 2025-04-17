import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Embedding, Flatten, Concatenate
from tensorflow.keras.models import Model
import pickle
import os

class PriceModel:
    def __init__(self):
        self.df = None
        self.operation = None
        self.clusters_map = None
        self.k_clusters = None
        self.dataset = None
        self.additional_dataset = None
        self.embedding_vector_size = 10
        self.test_size = 0.2
        self.valid_size = 0.2
        self.ann_epochs = 100
        self.ann_bs = 32
        self.ann_layers = [
            ('relu', 64),
            ('relu', 64),
            (None, 1)
        ]
        self.ann_early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            restore_best_weights=True,
            patience=5
            )
        self.price_model = None
        self.additional_model = None
        self.features_scaler = None
        self.target_scaler = None
        self.training_cols = None
        self.additional_training_cols = None

    def models_training(self, df, operation):
        # Load reference dataframe
        self.df = df.copy()
        self.operation = operation

        # Preprocess and split datasets #
        self.preprocess_data()

        # Split main price predictor set
        self.dataset, self.training_cols = self.split_data(
            self.df.drop(columns=['price']),
            self.df['price']
            )

        # Split additional price predictor set
        self.additional_dataset, self.additional_training_cols = self.split_data(
            self.df.drop(columns=['additional_costs','price']),
            self.df['additional_costs']
            )

        # Train price predictor ANN #
        self.price_model = self.train_ann(self.training_cols, self.dataset)

        # Train additional costs predictor ANN #
        self.additional_model = self.train_ann(self.additional_training_cols, self.additional_dataset)

        # # Save training results #
        self.save_models()

    def preprocess_data(self):
        # Convert location using dummies #
        self.convert_location()

        # Standardize numeric features #
        self.standardize_features()

        # Hot encode type col #
        self.encode_types()

    def convert_location(self):
        """ Convert location using one-hot encoding dummies """
        # Get dummies
        location_dummies = pd.get_dummies(self.df['location'], prefix='location', drop_first=False)

        # Map to 0 and 1
        location_dummies = location_dummies.map(lambda x: 1 if x > 0 else 0)

        # Update df
        self.df = pd.concat([self.df, location_dummies], axis=1)
        self.df.drop(['location'], axis=1, inplace=True)

    def standardize_features(self):
        """Standardizes the numeric features in the DataFrame."""
        self.features_scaler = StandardScaler()
        self.target_scaler = StandardScaler()
        features_to_standardize = ['size', 'dorms', 'toilets', 'garage', 'additional_costs']

        # Fit and transform the numeric features
        self.df[features_to_standardize] = self.features_scaler.fit_transform(self.df[features_to_standardize])
        self.df['price'] = self.target_scaler.fit_transform(self.df[['price']])


    def encode_types(self):
        """One-hot encodes the 'type' column in the DataFrame."""
        # Get dummies
        type_dummies = pd.get_dummies(self.df['type'], prefix='type', drop_first=False)

        # Map to 0 and 1
        type_dummies = type_dummies.map(lambda x: 1 if x > 0 else 0)

        # Update df
        self.df = pd.concat([self.df, type_dummies], axis=1)
        self.df.drop(['type'], axis=1, inplace=True)

    def split_data(self, X, y):
        training_cols = X.columns

        X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=self.test_size,
                                                                              random_state=42)
        X_train, X_valid, y_train, y_valid = train_test_split(X_train_val, y_train_val,
                                                                                  test_size=self.valid_size,
                                                                                  random_state=42)

        return {'X_train': X_train, 'X_valid':X_valid, 'X_test':X_test, 'y_train':y_train, 'y_valid':y_valid, 'y_test':y_test}, training_cols

    def train_ann(self, training_cols, dataset):
        """Trains an Artificial Neural Network"""

        # Define input layer
        input_layer = Input(shape=(len(training_cols),))
        x = input_layer

        # Stack ANN layers dynamically
        for activation, units in self.ann_layers:
            x = Dense(units=units, activation=activation)(x)

        # Build and compile model
        model = Model(inputs=input_layer, outputs=x)
        model.compile(optimizer='adam', loss='mean_squared_error')

        # Prepare input features
        X_train = dataset['X_train'][training_cols].values
        X_valid = dataset['X_valid'][training_cols].values

        # Fit the model
        model.fit(
            X_train,
            dataset['y_train'],
            epochs=self.ann_epochs,
            batch_size=self.ann_bs,
            validation_data=(X_valid, dataset['y_valid']),
            callbacks=[self.ann_early_stopping],
            verbose=0
        )

        return model

    def save_models(self):
      """Saves trained models, encoders, and column info."""
      # Initiate directories
      base_dir = f'data/{self.operation}'
      if not os.path.exists(base_dir):
          os.makedirs(base_dir)

      with open(f'{base_dir}/price_model.pkl', 'wb') as file:
          pickle.dump(self.price_model, file)

      with open(f'{base_dir}/additional_model.pkl', 'wb') as file:
          pickle.dump(self.additional_model, file)

      with open(f'{base_dir}/encoders.pkl', 'wb') as file:
          pickle.dump({
              'features_scaler': self.features_scaler,
              'target_scaler': self.target_scaler
          }, file)

      if self.clusters_map and self.k_clusters:
        # Save location info
        with open(f'{base_dir}/location.pkl', 'wb') as file:
            pickle.dump({
                'clusters_map': self.clusters_map,
                'k_clusters': self.k_clusters
            }, file)

    def load_models(self, operation):
        try:
            """Loads trained models, encoders, and column info."""
            base_dir = f'data/{operation}'
            if not os.path.exists(base_dir):
                raise Exception("Directory not found")

            with open(f'{base_dir}/price_model.pkl', 'rb') as file:
                self.price_model = pickle.load(file)

            with open(f'{base_dir}/additional_model.pkl', 'rb') as file:
                self.additional_model = pickle.load(file)

            with open(f'{base_dir}/encoders.pkl', 'rb') as file:
                encoders = pickle.load(file)
                self.features_scaler = encoders['features_scaler']
                self.target_scaler = encoders['target_scaler']

            with open(f'{base_dir}/location.pkl', 'rb') as file:
                location_data = pickle.load(file)
                self.k_clusters = location_data['k_clusters']
                if self.k_clusters is None:
                  raise Exception("k_clusters not found in location data")
            
        except Exception as e:
            print(f"Error loading models: {e}")
            raise Exception("Error in loading models")

    def make_prediction(self, input_data):
        """Makes a prediction based on input data."""
        try:
            if not input_data["operation"] or input_data["operation"] == "":
                raise Exception("Operation not sent")

            # Load models and scalers
            self.load_models(input_data["operation"])

            # Prepare numeric and categorical input
            numeric_features = np.array([[
                input_data['size'],
                input_data['dorms'],
                input_data['toilets'],
                input_data['garage'],
                0  # placeholder for additional_costs
            ]])

            # Scale numeric features
            numeric_scaled = self.features_scaler.transform(numeric_features)

            # Prepare location vector (one-hot)
            location_vector = np.zeros((1, self.k_clusters))
            loc_idx = input_data['location']
            if 0 <= loc_idx < self.k_clusters:
                location_vector[0, loc_idx] = 1
            else:
                raise Exception(f"Invalid location index: {loc_idx}")

            # Prepare type vector (already one-hot encoded)
            types_vector = np.array(input_data['type']).reshape(1, -1)

            # --- Predict additional costs ---
            additional_input = np.concatenate([
                numeric_scaled[:, :-1],  # exclude placeholder additional_costs
                location_vector,
                types_vector
            ], axis=1)

            additional_pred = self.additional_model.predict(additional_input, verbose=0)

            # Add predicted additional_costs to the scaled numeric features
            numeric_scaled[0, -1] = additional_pred[0][0]

            # --- Predict price ---
            price_input = np.concatenate([
                numeric_scaled,
                location_vector,
                types_vector
            ], axis=1)

            price_pred = self.price_model.predict(price_input, verbose=0)

            # Inverse transform predictions
            price = self.target_scaler.inverse_transform(price_pred)[0][0]
            additional_cost = self.features_scaler.inverse_transform([[0, 0, 0, 0, additional_pred[0][0]]])[0][4]

            # Convert np to int
            return {
                'operation': input_data["operation"],
                'predicted_price': int(np.round(price, 0)),
                'predicted_additional_costs': int(np.round(additional_cost, 0))
            }

        except Exception as e:
            print(f"Error making prediction: {e}")
            return 'Error in making prediction'

