import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Embedding, Flatten, Concatenate
from tensorflow.keras.models import Model
import pickle
import geohash
import os

class PriceModel:
    def __init__(self):
        self.df = None
        self.operation = None
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
        self.label_encoder = None
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

        # Split additonal price predictor set
        self.additional_dataset, self.additional_training_cols = self.split_data(
            self.df.drop(columns=['additional_costs','price']),
            self.df['additional_costs']
            )
        
        # Train price predictor ANN #
        self.price_model = self.train_ann(self.training_cols, self.dataset)

        # Train additional costs predictor ANN #
        self.additional_model = self.train_ann(self.additional_training_cols, self.additional_dataset)

        # Save training results #
        self.save_models()

    def preprocess_data(self):
        # Convert location using dummies #
        self.convert_geohash()

        # Standardize numeric features #
        self.standardize_features()

        # Hot encode type col #
        self.encode_types()

    def convert_geohash(self):
        self.label_encoder = LabelEncoder()
        self.df['location'] = self.label_encoder.fit_transform(self.df['geohash'])
        self.df.drop(['geohash'], axis=1, inplace=True)

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
        """Trains an Artificial Neural Network with geohash embeddings."""
        # Inputs
        geohash_input = Input(shape=(1,), name="geohash")
        numeric_inputs = Input(shape=(len(training_cols)-1,), name="numeric_features")  # Excluding geohash

        # Geohash Embedding
        geohash_emb = Embedding(
            input_dim=len(self.label_encoder.classes_),  # Unique geohashes
            output_dim= self.embedding_vector_size
        )(geohash_input)
        geohash_emb = Flatten()(geohash_emb)

        # Merge geohash embedding with other inputs
        merged = Concatenate()([geohash_emb, numeric_inputs])

        # Stack ANN layers dynamically
        x = merged
        for layer in self.ann_layers:
            x = Dense(units=layer[1], activation=layer[0])(x)

        # Build model
        ann_model = Model(inputs=[geohash_input, numeric_inputs], outputs=x)

        # Compile model
        ann_model.compile(optimizer='adam', loss='mean_squared_error')

        # Prepare inputs for training dataset
        X_train_numeric = dataset['X_train'].drop(columns=['location']).values
        X_train_geohash = dataset['X_train']['location'].values

        X_valid_numeric = dataset['X_valid'].drop(columns=['location']).values
        X_valid_geohash = dataset['X_valid']['location'].values

        # Fit model #
        ann_model.fit(
            [X_train_geohash, X_train_numeric],
            dataset['y_train'],
            epochs=self.ann_epochs,
            batch_size=self.ann_bs,
            validation_data=([X_valid_geohash, X_valid_numeric], dataset['y_valid']),
            callbacks=[self.ann_early_stopping],
            verbose=0
        )

        return ann_model

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
              'label_encoder': self.label_encoder,
              'features_scaler': self.features_scaler,
              'target_scaler': self.target_scaler
          }, file)


    def load_models(self):
        try:
            """Loads trained models, encoders, and column info."""
            base_dir = f'data/{self.operation}'
            if not os.path.exists(base_dir):
                return 'Directory not found'

            with open(f'{base_dir}/price_model.pkl', 'rb') as file:
                self.price_model = pickle.load(file)

            with open(f'{base_dir}/additional_model.pkl', 'rb') as file:
                self.additional_model = pickle.load(file)

            with open(f'{base_dir}/encoders.pkl', 'rb') as file:
                encoders = pickle.load(file)
                self.label_encoder = encoders['label_encoder']
                self.features_scaler = encoders['features_scaler']
                self.target_scaler = encoders['target_scaler']

        except Exception as e:
            print(f"Error loading models: {e}")
            return 'Error in loading models'

    def make_prediction(self, input_data):
        """Makes a prediction based on input data."""
        # Load models
        if self.price_model is None or self.additional_model is None:
          print('Loading models...')
          try:
            self.load_models()
          except Exception as e:
            return 'Error in loading models'

        def encode_location(gh):
          """Encodes geohash, handling unknown values by finding the closest known one."""
          try:
              return self.label_encoder.transform([gh])[0]
          except ValueError:
              # Find closest known geohash
              lat, lon = geohash.decode(gh)
              closest_geohash = min(self.label_encoder.classes_, key=lambda known_gh: 
                  ((lat - geohash.decode(known_gh)[0]) ** 2 + (lon - geohash.decode(known_gh)[1]) ** 2) ** 0.5
              )
              return self.label_encoder.transform([closest_geohash])[0]
        
        # Encode location
        geohash_code = geohash.encode(input_data['location'][0], input_data['location'][1], precision=8)
        location_encoded = encode_location(geohash_code)
        
        # Create feature arrays for additional costs prediction
        additional_features = np.array([[
            input_data['size'],
            input_data['dorms'],
            input_data['toilets'],
            input_data['garage'],  
            0, # Initial dummy value
        ]])
        
        # Standardize numeric features
        additional_numeric_scaled = self.features_scaler.transform(additional_features)

        # Reshape types list
        types_feature = np.array(input_data['type']).reshape(1, -1)
        
        # Combine features into array
        additional_features_array = np.concatenate([
            additional_numeric_scaled[:, :-1],  # all except additional costs
            types_feature
        ], axis=1)
       
        # Predict additional costs
        additional_costs_pred = self.additional_model.predict([
            np.array([[location_encoded]]), # location = Embedding
            additional_features_array # features
        ])
      
        # Create feature arrays for price prediction (including predicted additional costs)
        price_features_array = np.concatenate([
            additional_numeric_scaled[:, :-1], 
            np.array([[additional_costs_pred[0][0]]]),
            types_feature
        ], axis=1)
        
        # Predict price
        price_pred = self.price_model.predict([
            np.array([[location_encoded]]),
            price_features_array
        ])
        
        # Inverse transform both predictions
        price_pred_original = self.target_scaler.inverse_transform(price_pred)[0][0]
        additional_cost_original = self.features_scaler.inverse_transform([[0,0,0,0,additional_costs_pred[0][0]]])[0][0]

        return {
            'predicted_price': np.round(price_pred_original, 0),
            'predicted_additional_costs': np.round(additional_cost_original,0)
        }