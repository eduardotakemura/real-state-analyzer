from flask import Blueprint, jsonify, request
from .models import Properties
from .utils import db_to_dict, query_with_filters

main = Blueprint('main', __name__)

@main.route('/all', methods=['GET'])
def get_all():
    properties = Properties.query.all()
    clean_properties = db_to_dict(properties)

    return jsonify(clean_properties), 200

@main.route('/filter/count', methods=['GET'])
def get_count_with_filter():
    try:
        response = query_with_filters(request.args.to_dict())
        return jsonify(len(response)), 200

    except Exception as e:
        print(f"An error occured: {e}")
        return jsonify(e), 400

@main.route('/filter', methods=['GET'])
def get_with_filter():
    try:
        response = query_with_filters(request.args.to_dict())
        return jsonify(response), 200

    except Exception as e:
        print(f"An error occured: {e}")
        return jsonify(e), 400
