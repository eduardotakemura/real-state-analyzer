import pandas as pd
from models import analyzer, preprocessor

# Load data from CSV
def load_data():
    df = pd.read_csv('data/data.csv')
    return df

# Extract unique values for the dropdowns
def _extract_initial(data):
    operations = data['operation'].unique().tolist()
    property_types = ['All'] + data['type'].unique().tolist()
    states = data['state'].unique().tolist()
    cities = data['city'].unique().tolist()
    neighborhoods = ['All'] + data['neighborhood'].unique().tolist()
    dorms = ['1+', '2+', '3+']
    toilets = ['1+', '2+', '3+']
    garages = ['1+', '2+', '3+']
    min_size = data['size'].min()
    max_size = data['size'].max()
    min_price = data['price'].min()
    max_price = data['price'].max()

    return {
        'operation': operations,
        'type': property_types,
        'state': states,
        'city': cities,
        'neighborhood': neighborhoods,
        'dorms': dorms,
        'toilets': toilets,
        'garages': garages,
        'min_size': min_size,
        'max_size': max_size,
        'min_price': min_price,
        'max_price': max_price
    }

# Backend logic to prepare dropdown data
def get_initial_options():
    initial_options = _extract_initial(df)
    return initial_options

def _filter_data(data, filters):
    data_filtered = data[
        (data['operation'] == filters["operation"]) &
        ((filters['type'] == "All") | (data['type'] == filters["type"])) &
        (data['state'] == filters["state"]) &
        (data['city'] == filters["city"]) &
        ((filters["neighborhood"] == "All") | (data['neighborhood'] == filters["neighborhood"])) &
        (data['dorms'] >= int(filters["dorms"].replace('+', ''))) &  # Handle '1+' for dorms
        (data['toilets'] >= int(filters["toilets"].replace('+', ''))) &  # Handle '1+' for toilets
        (data['garage'] >= int(filters["garages"].replace('+', ''))) &  # Handle '1+' for garages
        (data['size'] >= filters["min_size"]) &
        (data['size'] <= filters["max_size"]) &
        (data['price'] >= filters["min_price"]) &
        (data['price'] <= filters["max_price"])
        ]
    return data_filtered

def _run_analyzer(data):
    summary_by_type = analyzer.summarize_by_type(data)
    type_distribution = analyzer.type_distribution(data)
    summary_by_location = analyzer.summarize_by_location(data)
    location_plots = analyzer.location_plots(data)
    return summary_by_type, type_distribution, summary_by_location, location_plots


def get_report(filters):
    # Filter df based on requested filters #
    df_filtered = _filter_data(df, filters)

    # Preprocess df #
    df_preprocessed = preprocessor.process_df(df_filtered)

    # Report Summary #
    report_summary = pd.DataFrame([
        len(df_preprocessed),
        preprocessor.current_operation,
        df_preprocessed['location'].max() + 1
    ],index=['Entries Processed','Operation','Number of Locations Selected'])

    # Run the Analyzer #
    summary_by_type, type_distribution, summary_by_location, location_plots = _run_analyzer(df_preprocessed)

    # Get Clusters location and Price heatmap from preprocessor #
    clusters_map = preprocessor.clusters_map
    price_heatmap = preprocessor.price_heatmap

    return (summary_by_type, type_distribution, summary_by_location, location_plots, clusters_map,
            price_heatmap, report_summary)

df = load_data()
analyzer = analyzer.Analyzer()
preprocessor = preprocessor.Preprocessor()
