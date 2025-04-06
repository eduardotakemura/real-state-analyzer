import geohash
from scipy.stats.mstats import winsorize

class Preprocessor:
    def __init__(self):
        self.data = None
        self.current_operation = None
        self.geohash_precision = 8

    def process_df(self, df):
        """ Full pipeline to process the data. """
        # Check current operation #
        self.current_operation = self.extract_operation(df)

        # Drop unnecessary features #
        self.data = self.drop_unrelevant(df)

        # Drop Empty Lat,Lng #
        self.data = self.drop_empty_loc(self.data)

        # Map type feature #
        self.data = self.map_types(self.data)

        # Remove outliers #
        self.data = self.remove_outliers(self.data, self.drop_outliers)

        # Geohash location
        self.data = self.geohash_location(self.data, self.geohash_precision)

        return self.data

    def extract_operation(self, df):
        operations = list(df['operation'].unique())
        return operations[0]

    def drop_unrelevant(self, df):
        features_to_drop = ['id', 'link', 'operation', 'street', 'neighborhood', 'city','page_id', 'scraping_date']
        df = df.drop(features_to_drop, axis=1)
        return df

    def drop_empty_loc(self, df):
        df = df[df['latitude'] != 0.0]
        df = df[df['longitude'] != 0.0]
        return df

    def map_types(self, df):
        # Casa = 0, Apartamento = 1, Terreno = 2, Comercial = 3, Fazenda = 4, Outros = 5
        type_map = {
            'Casa': 0,
            'Apartamento': 1,
            'Casa de Condomínio': 0,
            'Cobertura': 1,
            'Flat': 1,
            'Kitnet/Conjugado': 1,
            'Lote/Terreno': 2,
            'Sobrado': 0,
            'Edifício Residencial': 3,
            'Fazenda/Sítios/Chácaras': 4,
            'Consultório': 3,
            'Galpão/Depósito/Armazém': 3,
            'Imóvel Comercial': 3,
            'Lote/Terreno': 2,
            'Ponto Comercial/Loja/Box': 3,
            'Sala/Conjunto': 3,
            'Prédio/Edifício Inteiro': 3,
        }
        df['type'] = df['type'].map(type_map)

        # Fill NaN with 5 = not defined maps
        df['type'] = df['type'].fillna(5)

        # Cast to int
        df['type'] = df['type'].astype(int)

        return df

    def geohash_location(self, df, precision):
        df['geohash'] = df.apply(lambda row: geohash.encode(row['latitude'], row['longitude'], precision=precision), axis=1)
        df.drop(['latitude', 'longitude'], axis=1, inplace=True)
        return df

    def remove_outliers(self, df):
        for col in df.select_dtypes(include=['number']).columns:
            df[col] = winsorize(df[col], limits=[0.05, 0.05])
        
        return df