from flask import Blueprint, jsonify, request
import requests
import pandas as pd
from .utils import extract_initial_fields, filtered_query, analise_data, preprocess_data, load_model

# Define a blueprint
main_blueprint = Blueprint('main', __name__)

# Load models at app init
selling_model, renting_model = load_model()

@main_blueprint.route('/initial', methods=['GET'])
def get_initial():
    """ Fetch data from API to fill initial form """
    endpoint = 'http://127.0.0.1:4000/all'
    response = requests.get(url=endpoint)
    data = response.json()

    return jsonify(extract_initial_fields(data))

@main_blueprint.route('/get_entries_count', methods=['POST'])
def get_entries_count():
    """ Query API for entries count for selected filters. """
    data = request.json
    for key in {'entries','update','operations','types','states','cities','neighborhoods','dorms','toilets','garages'}:
        data.pop(key,None)

    endpoint = 'http://127.0.0.1:4000/filter/count'
    response = requests.get(
        url=endpoint,
        params= {
            'operation':data['operation'],
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
    data = response.json()

    return jsonify({'entries_count': data})

@main_blueprint.route('/get_analysis', methods=['POST'])
def get_analysis():
    """ Process analysis with selected filters. """
    data = filtered_query(request.json)

    preprocessor, df_processed, df = preprocess_data(data)
    (total_entries, operation, locations_clusters, summary_by_type, type_distribution,
     summary_by_location, location_plots, clusters_map, price_heatmap) = analise_data(preprocessor, df_processed, df)

    return jsonify({
        'total_entries': total_entries,
        'operation': operation,
        'locations_clusters': locations_clusters,
        'summary_by_type': summary_by_type,
        'type_distribution': type_distribution,
        'summary_by_location': summary_by_location,
        'locations_plots': location_plots,
        'clusters_map':clusters_map,
        'price_heatmap':price_heatmap
    })

@main_blueprint.route('/get_prediction', methods=['POST'])
def get_prediction():
    """ Make a prediction based on the given inputs. """
    data = request.json
    operation = data['operation']

    data.pop('operation')
    input_data = {key: int(value) for key, value in data.items()}

    if operation == 'selling':
        prediction = selling_model.predict(input_data)

    else:
        prediction = renting_model.predict(input_data)

    return jsonify({
        'prediction': float(prediction)
    })




