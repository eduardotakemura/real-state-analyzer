from .models import Properties

def query_with_filters(requested_filters):
    """ Query the API using filters. """
    # Initiate filters list #
    filters = []

    # Deconstruct input dict #
    (operation, type, state, city, neighborhood, dorms, toilets, garages,
     min_size, max_size, min_price, max_price) = requested_filters.values()

    # Apply all individual filters to the query #
    filters.append(Properties.operation == operation)
    filters.append(Properties.state == state)
    filters.append(Properties.city == city)
    filters.append(Properties.dorms >= int(dorms))
    filters.append(Properties.toilets >= int(toilets))
    filters.append(Properties.garage >= int(garages))
    filters.append(Properties.size >= int(min_size))
    filters.append(Properties.size <= int(max_size))
    filters.append(Properties.price >= int(min_price))
    filters.append(Properties.price <= int(max_price))

    # Optional fields #
    if type != "All":
        filters.append(Properties.type == type)

    if neighborhood != "All":
        filters.append(Properties.neighborhood == neighborhood)

    # Query #
    results = Properties.query.filter(*filters).all()

    # Convert back to dictionary, and clean unicodes #
    response = db_to_dict(results)

    return response

def db_to_dict(data):
    data_dict = [
        {
            'id': prop.id,
            'link': prop.link,
            'title': prop.title,
            'operation': prop.operation,
            'address': prop.address,
            'size': prop.size,
            'dorms': prop.dorms,
            'toilets': prop.toilets,
            'garage': prop.garage,
            'price': prop.price,
            'additional_costs': prop.additional_costs,
            'features': prop.features,
            'type': prop.type,
            'street': prop.street,
            'neighborhood': prop.neighborhood,
            'city': prop.city,
            'state': prop.state,
            'latitude': prop.latitude,
            'longitude': prop.longitude,
            'page_id': prop.page_id,
            'scrapping_date': prop.scrapping_date
        }
        for prop in data
    ]

    cleaned_data_dict = clean_unicode(data_dict)
    return cleaned_data_dict

def clean_unicode(data):
    if isinstance(data, str):
        return data  # Skip encoding/decoding if it's already correct
    elif isinstance(data, dict):
        return {k: clean_unicode(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_unicode(i) for i in data]
    else:
        return data