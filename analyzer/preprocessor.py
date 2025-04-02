import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from kneed import KneeLocator
import folium
from folium.plugins import HeatMap

class Preprocessor:
    def __init__(self):
        self.data = None
        self.current_operation = None
        self.drop_loc_outliers = True
        self.distance_radius = None
        self.k_cluster = None
        self.k_limit = 20
        self.clusters_plot = False
        self.target = 'price'
        self.split_threshold = 0.05
        self.clusters_map = None
        self.price_heatmap = None
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

        # Map types #
        self.data = self.map_types(self.data)

        # Location Clustering #
        ## First drop outliers #
        if self.drop_loc_outliers:
            self.data = self.drop_location_outliers(self.data, self.distance_radius)

        ## Clustering ##
        self.data = self.location_clustering(self.data, self.k_cluster, self.k_limit, self.clusters_plot)

        # Generate the clusters map #
        self.clusters_map = self._create_clusters_map(self.data)

        # Generate the heat map #
        self.price_heatmap = self.generate_price_heatmap(df)

        # Drop lat/lng features #
        self.data.drop(columns=['latitude', 'longitude'], inplace=True)

        # Add price/sqm as feature #
        self.data = self.add_price_per_sqm(self.data)

        # Remove outliers #
        self.data = self.remove_outliers(self.data)

        return self.data

    def extract_operation(self, df):
        operations = list(df['operation'].unique())
        return operations[0]

    def drop_unrelevant(self, df):
        features_to_drop = ['id', 'link', 'operation', 'street', 'neighborhood', 'city',
                            'page_id', 'scrapping_date']
        df = df.drop(features_to_drop, axis=1)
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

        # Map types #
        df['type'] = df['type'].map(type_map)

        # Fill NaN with 5 = not defined maps
        df['type'] = df['type'].fillna(5)
        return df

    def drop_location_outliers(self, df, distance_radius=None):
        if distance_radius is None:

            # Dynamically set the radius based on the data spread #
            lat_range = df['latitude'].max() - df['latitude'].min()
            lng_range = df['longitude'].max() - df['longitude'].min()
            max_range = max(lat_range, lng_range)

            # Set radius based on the max range #
            if max_range < 1:  # Neighborhood
                distance_radius = 2  # in km
            elif max_range < 5:  # Small Cities
                distance_radius = 10
            elif max_range < 10:  # Large Cities
                distance_radius = 20
            else:  # Large area
                distance_radius = 50

        # Calculate margins based on the chosen distance radius
        lat_margin = distance_radius / 110.574
        lng_margin = distance_radius / (111.320 * np.cos(np.radians(df['latitude'].mean())))

        # Calculate bounds with a margin
        lat_mean = df['latitude'].mean()
        lng_mean = df['longitude'].mean()

        lat_min = lat_mean - lat_margin
        lat_max = lat_mean + lat_margin

        lng_min = lng_mean - lng_margin
        lng_max = lng_mean + lng_margin

        # Filter rows that fall within the dynamically calculated bounds
        df = df[(df['latitude'] >= lat_min) & (df['latitude'] <= lat_max)]
        df = df[(df['longitude'] >= lng_min) & (df['longitude'] <= lng_max)]

        return df

    def location_clustering(self, df, k_cluster=None, k_limit=20, plot=False):
        # Extract and Standardize features #
        x_scaled = self.standardize_location(df)

        # Apply K-Means clustering with the optimal number of clusters or requested k value #
        if k_cluster:
            kmeans = KMeans(n_clusters=k_cluster, random_state=0)
        else:
            optimal_k = self.determine_optimal_k(x_scaled, k_limit, plot)
            kmeans = KMeans(n_clusters=optimal_k, random_state=0)
            self.k_cluster = optimal_k

        # Merge with df #
        df['location'] = kmeans.fit_predict(x_scaled)

        # Plot Clusters #
        if plot:
            self.plot_clusters(df)

        return df

    def standardize_location(self, df):
        x = df[['latitude', 'longitude']]
        scaler = StandardScaler()
        x_scaled = scaler.fit_transform(x)

        return x_scaled

    def determine_optimal_k(self, x_scaled, k_limit, plot=False):
        wcss = []
        for i in range(1, k_limit):
            kmeans = KMeans(n_clusters=i, n_init='auto', random_state=0)
            kmeans.fit(x_scaled)
            wcss.append(kmeans.inertia_)

        if plot:
            plt.figure(figsize=(10, 6))
            plt.plot(range(1, k_limit), wcss, marker='o')
            plt.title('The Elbow Method')
            plt.xlabel('Number of clusters')
            plt.ylabel('WCSS')
            plt.grid(True)
            plt.show()

        # Identify the elbow point (the optimal k) #
        optimal_k = self.find_elbow_point(wcss)
        return optimal_k

    def find_elbow_point(self, wcss):
        kl = KneeLocator(range(1, len(wcss) + 1), wcss, curve='convex', direction='decreasing')
        optimal_k = kl.elbow
        return optimal_k

    def plot_clusters(self, df):
        plt.scatter(df['latitude'], df['longitude'], c=df['location'], cmap='viridis')
        plt.colorbar(label='Cluster')
        plt.xlabel('Latitude')
        plt.ylabel('Longitude')
        plt.title('Result Clustering')
        plt.show()

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
        #mymap.save('clusters_map.html')

        return mymap._repr_html_()

    def add_price_per_sqm(self, df):
        df['price_per_sqm'] = df['price'] / df['size']
        return df

    def generate_price_heatmap(self, df):
        """Generate a heatmap based on property prices."""
        map_center = [df['latitude'].mean(), df['longitude'].mean()]
        price_heatmap = folium.Map(location=map_center, zoom_start=11)

        # Prepare data for heatmap
        heat_data = [[row['latitude'], row['longitude'], row['price']] for index, row in df.iterrows()]
        HeatMap(heat_data).add_to(price_heatmap)
        #price_heatmap.save('price_heatmap.html')

        return price_heatmap._repr_html_()

    def remove_outliers(self, df):
        Q1 = df.quantile(self.outliers_config['Q1'])
        Q3 = df.quantile(self.outliers_config['Q3'])
        IQR = Q3 - Q1
        lower_bound = Q1 - self.outliers_config['multiplier'] * IQR
        upper_bound = Q3 + self.outliers_config['multiplier'] * IQR

        return df[~((df < lower_bound) | (df > upper_bound)).any(axis=1)]

