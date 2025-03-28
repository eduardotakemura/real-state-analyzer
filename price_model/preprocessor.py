import pandas as pd
import geohash

class Preprocessor:
    def __init__(self):
        self.data = None
        self.current_operation = None
        self.geohash_precision = 8
        self.target = 'price'
        self.split_threshold = 0.05
        self.drop_outliers = True
        self.outliers_config = {
            'multiplier': 1.5,
            'Q1': 0.25,
            'Q3': 0.85
        }

    def process_df(self, df):
        """ Full pipeline to process the data. """
        # Check current operation #
        self.current_operation = self.extract_operation(df)

        # Drop unnecessary features #
        self.data = self.drop_unrelevant(df)

        # Map type feature: Apartaments = 1, Houses = 0 #
        self.data = self.map_types(self.data)

        # Split features #
        self.data = self.split_features_col(self.data)

        # Drop low correlation features #
        self.data = self.drop_low_correlation_features(self.data, self.target, self.split_threshold)

        # Remove outliers #
        self.data = self.remove_outliers(self.data, self.drop_outliers)

        # Geohash location
        self.data = self.geohash_location(self.data, self.geohash_precision)

        return self.data

    def extract_operation(self, df):
        operations = list(df['operation'].unique())
        return operations[0]

    def drop_unrelevant(self, df):
        features_to_drop = ['id', 'link', 'title', 'operation', 'address', 'street', 'neighborhood', 'city', 'state',
                            'page_id', 'scrapping_date']
        df = df.drop(features_to_drop, axis=1)
        return df

    def map_types(self, df):
        df['type'] = df['type'].map({'Apartamento': 1, 'Casa': 0})
        return df

    def geohash_location(self, df, precision):
        df['geohash'] = df.apply(lambda row: geohash.encode(row['latitude'], row['longitude'], precision=precision), axis=1)
        df.drop(['latitude', 'longitude'], axis=1, inplace=True)
        return df


    def split_features_col(self, df):
        df['feature_list'] = df['features'].apply(
            lambda x: [feature.strip() for feature in x.split(',')] if pd.notna(x) else [])

        unique_features = set(feature for sublist in df['feature_list'] for feature in sublist)

        for feature in unique_features:
            df[feature] = df['feature_list'].apply(lambda x: 1 if feature in x else 0)

        df.drop(columns=['feature_list', 'features'], inplace=True)

        return df

    def drop_low_correlation_features(self, df, target_col='price', threshold=0.05):
        ref_cols = ['size', 'dorms', 'toilets', 'garage', 'price', 'additional_costs', 'type', 'latitude','longitude']
        cols_to_drop = [col for col in df.columns if col not in ref_cols]

        # Calculate correlation matrix
        corr_matrix = df.corr()

        # Extract correlations with the target variable
        corr_with_target = corr_matrix[target_col]

        # Filter features based on the correlation threshold
        low_corr_features = corr_with_target[cols_to_drop][abs(corr_with_target[cols_to_drop]) < threshold].index

        # Drop low correlation features
        df = df.drop(columns=low_corr_features)

        return df

    def remove_outliers(self, df, drop_outliers):
        if not drop_outliers:
            return df

        df = df.copy()
        Q1 = df.quantile(self.outliers_config['Q1'])
        Q3 = df.quantile(self.outliers_config['Q3'])
        IQR = Q3 - Q1
        lower_bound = Q1 - self.outliers_config['multiplier'] * IQR
        upper_bound = Q3 + self.outliers_config['multiplier'] * IQR

        return df[~((df < lower_bound) | (df > upper_bound)).any(axis=1)]

