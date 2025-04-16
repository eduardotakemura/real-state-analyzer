from scipy.stats.mstats import winsorize
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from kneed import KneeLocator
import folium
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

class Preprocessor:
    def __init__(self):
        self.data = None
        self.current_operation = None
        self.clusters_map = None
        self.k_clusters = None

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

        # Remove location outliers #
        self.data = self.drop_location_outliers(self.data)

        ## Clustering ##
        self.data = self.location_clustering(self.data)

        # Generate the clusters map #
        self.clusters_map = self._create_clusters_map(self.data)

        # Drop lat,lng #
        self.data = self.data.drop(['latitude', 'longitude'], axis=1)

        # Remove outliers #
        self.data = self.remove_outliers(self.data)

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
        # Casa = 0, Apartamento = 1
        type_map = {
            'Casa': 0,
            'Apartamento': 1,
            'Casa de Condomínio': 0,
            'Cobertura': 1,
            'Flat': 1,
            'Kitnet/Conjugado': 1,
            'Lote/Terreno': 0,
            'Sobrado': 0,
            'Edifício Residencial': 0,
            'Fazenda/Sítios/Chácaras': 0,
            'Consultório': 0,
            'Galpão/Depósito/Armazém': 0,
            'Imóvel Comercial': 0,
            'Lote/Terreno': 0,
            'Ponto Comercial/Loja/Box': 0,
            'Sala/Conjunto': 0,
            'Prédio/Edifício Inteiro': 0,
        }
        df['type'] = df['type'].map(type_map)

        # Drop NaN
        df = df.dropna(subset=['type'])

        # Cast to int
        df['type'] = df['type'].astype(int)

        return df

    def location_clustering(self, df, k_cluster=None, k_limit=20):
        # Extract and Standardize features #
        x_scaled = self.standardize_location(df)

        # Apply K-Means clustering with the optimal number of clusters or requested k value #
        if k_cluster:
            kmeans = KMeans(n_clusters=k_cluster, random_state=0)
        else:
            optimal_k = self.determine_optimal_k(x_scaled, k_limit)
            kmeans = KMeans(n_clusters=optimal_k, random_state=0)
            self.k_clusters = optimal_k

        # Merge with df #
        df['location'] = kmeans.fit_predict(x_scaled)

        return df

    def standardize_location(self, df):
        x = df[['latitude', 'longitude']]
        scaler = StandardScaler()
        x_scaled = scaler.fit_transform(x)

        return x_scaled

    def determine_optimal_k(self, x_scaled, k_limit):
        wcss = []
        for i in range(1, k_limit):
            kmeans = KMeans(n_clusters=i, n_init='auto', random_state=0)
            kmeans.fit(x_scaled)
            wcss.append(kmeans.inertia_)

        # Identify the elbow point (the optimal k) #
        optimal_k = self.find_elbow_point(wcss)
        return optimal_k

    def find_elbow_point(self, wcss):
        kl = KneeLocator(range(1, len(wcss) + 1), wcss, curve='convex', direction='decreasing')
        optimal_k = kl.elbow
        return optimal_k

    def _create_clusters_map(self, df):
        """Create a folium map with observation points, highlighting clusters, and save it."""
        map_center = [df['latitude'].mean(), df['longitude'].mean()]
        mymap = folium.Map(location=map_center, zoom_start=11)

        # Generate a list of colors for different clusters using matplotlib
        num_clusters = len(df['location'].unique())
        cmap = plt.cm.get_cmap('tab10', num_clusters)
        cluster_colors = {cluster: mcolors.rgb2hex(cmap(cluster / num_clusters)) for cluster in df['location'].unique()}

        # Add points to the map with cluster-specific colors
        for index, row in df.iterrows():
            cluster = row['location']
            color = cluster_colors[cluster]
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=5,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                popup=f'Cluster: {cluster}'
            ).add_to(mymap)

        # Add a legend to the map
        legend_html = '''
        <div style="position: fixed;
                    bottom: 50px; left: 50px; width: 150px; height: auto;
                    border:2px solid grey; z-index:9999; font-size:14px;
                    background-color:white; opacity: 0.85;">
        <strong> Locations: </strong><br>
        '''
        for cluster, color in cluster_colors.items():
            legend_html += f'<i style="background:{color};width:20px;height:20px;float:left;margin-right:10px;"></i>Location {cluster}<br>'

        legend_html += '</div>'
        mymap.get_root().html.add_child(folium.Element(legend_html))

        return mymap._repr_html_()

    def drop_location_outliers(self, df, distance_radius=20):
      from math import radians, cos, sin, asin, sqrt

      def haversine(lat1, lon1, lat2, lon2):
          # Convert decimal degrees to radians
          lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
          # Haversine formula
          dlat = lat2 - lat1
          dlon = lon2 - lon1
          a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
          c = 2 * asin(sqrt(a))
          r = 6371  # Radius of earth in kilometers
          return c * r

      center_lat = df['latitude'].median()
      center_lon = df['longitude'].median()

      df['distance_from_center'] = df.apply(
          lambda row: haversine(center_lat, center_lon, row['latitude'], row['longitude']), axis=1
      )

      df = df[df['distance_from_center'] <= distance_radius]
      df = df.drop(columns='distance_from_center')

      return df

    def remove_outliers(self, df, multiplier=1.5, q1=0.25, q3=0.85):
        Q1 = df.quantile(q1)
        Q3 = df.quantile(q3)
        IQR = Q3 - Q1
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR

        return df[~((df < lower_bound) | (df > upper_bound)).any(axis=1)]