from models import Analyzer, ModelPreprocessor, PriceModel
import pandas as pd
import io
import base64
import requests

def extract_initial_fields(data):
    """ Extract base fields from API response """
    min_size, max_size = get_min_max(data, 'size')
    min_price, max_price = get_min_max(data, 'price')

    return ({
        'entries': len(data),
        'update': get_unique(data, 'scrapping_date')[0],
        'operations': get_unique(data, 'operation'),
        'types': ['All'] + get_unique(data, 'type'),
        'states': get_unique(data, 'state'),
        'cities': get_unique(data, 'city'),
        'neighborhoods': ['All'] + get_unique(data, 'neighborhood'),
        'dorms':['1+', '2+', '3+', '4+'],
        'toilets':['1+', '2+', '3+', '4+'],
        'garages':['1+', '2+', '3+', '4+'],
        'min_size': min_size,
        'max_size': max_size,
        'min_price': min_price,
        'max_price': max_price
    })

def get_unique(data, field):
    """Extracts unique values from the data for a given field."""
    return sorted(set([item[field] for item in data]))

def get_min_max(data, field):
    """Extracts the min and max values for a given field from the data."""
    values = [item[field] for item in data]
    return min(values), max(values)

def filtered_query(params):
    # Filter params to only those which gonna be sent to the API #
    data = params
    for key in {'entries', 'update', 'operations', 'types', 'states', 'cities',
                'neighborhoods', 'dorms', 'toilets', 'garages'}:
        data.pop(key, None)

    # Query the API #
    endpoint = 'http://127.0.0.1:4000/filter'
    response = requests.get(
        url=endpoint,
        params={
            'operation': data['operation'],
            'type': data['type'],
            'state': data['state'],
            'city': data['city'],
            'neighborhood': data['neighborhood'],
            'dorms': data['dorm'].split('+')[0],
            'toilets': data['toilet'].split('+')[0],
            'garages': data['garage'].split('+')[0],
            'min_size': data['min_size'],
            'max_size': data['max_size'],
            'min_price': data['min_price'],
            'max_price': data['max_price']
        }
    )
    return response.json()

def preprocess_data(data):
    df = pd.DataFrame(data)
    preprocessor = ModelPreprocessor()
    df_processed = preprocessor.process_df(df)

    return preprocessor, df_processed, df

def analise_data(preprocessor, df_processed, df):
    analyzer = Analyzer()
    total_entries, operation, locations_clusters = _main_summary(df_processed, df)
    summary_by_type, type_distribution = _type_summary(analyzer, df_processed)
    summary_by_location, location_plots = _location_summary(analyzer, df_processed)
    clusters_map = preprocessor.clusters_map
    price_heatmap = preprocessor.price_heatmap

    return (total_entries, operation, locations_clusters, summary_by_type, type_distribution,
            summary_by_location, location_plots, clusters_map, price_heatmap)

def _main_summary(df_processed, df):
    total_entries = df_processed.shape[0]
    operation = df['operation'][0]
    locations_clusters = df_processed['location'].nunique()

    return total_entries, operation, locations_clusters

def _type_summary(analyzer, df_processed):
    # Summary by Type Table #
    summary_by_type = analyzer.summarize_by_type(df_processed)
    summary_by_type = summary_by_type.to_dict(orient='records')

    # Type Distribution fig #
    type_distr_fig = analyzer.type_distribution(df_processed)
    img = io.BytesIO()
    type_distr_fig.savefig(img, format='png')
    img.seek(0)
    type_distr_base64 = base64.b64encode(img.getvalue()).decode('utf8')

    return summary_by_type, type_distr_base64

def _location_summary(analyzer, df_processed):
    # Summary by Location Table #
    summary_by_location = analyzer.summarize_by_location(df_processed)
    summary_by_location = summary_by_location.to_dict(orient='records')

    # Location Distribution fig #
    locations_fig = analyzer.location_plots(df_processed)
    img = io.BytesIO()
    locations_fig.savefig(img, format='png')
    img.seek(0)
    locations_fig_base64 = base64.b64encode(img.getvalue()).decode('utf8')

    return summary_by_location, locations_fig_base64

def load_model():
    selling_model = PriceModel.load_model(
        f"data/model/selling_model.h5",
        f"data/model/selling_scaler.pkl",
        f"data/model/selling_config.json")
    renting_model = PriceModel.load_model(
        f"data/model/renting_model.h5",
        f"data/model/renting_scaler.pkl",
        f"data/model/renting_config.json")
    return selling_model, renting_model






