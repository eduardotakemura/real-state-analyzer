import streamlit as st
from streamlit_folium import folium_static
from server import get_initial_options, get_report, get_prediction

def render_form(fields_options):
    # Header #
    st.title("Real Estate Analyzer")
    st.subheader("Assess Real State Insights and Predict Selling and Renting Prices")
    st.markdown("---")

    # Form Dropdown Buttons #
    operation = st.selectbox('Operation', fields_options['operation'])
    property_type = st.selectbox('Type', fields_options['type'])
    state = st.selectbox('State', fields_options['state'])
    city = st.selectbox('City', fields_options['city'])
    neighborhood = st.selectbox('Neighborhood', fields_options['neighborhood'])
    dorms = st.selectbox('Number of Dorms', fields_options['dorms'])
    toilets = st.selectbox('Number of Toilets', fields_options['toilets'])
    garages = st.selectbox('Number of Garages', fields_options['garages'])

    # Size and Price Range Fields #
    min_size = st.number_input('Min Size (sqm)', value=fields_options['min_size'], step=1)
    max_size = st.number_input('Max Size (sqm)', value=fields_options['max_size'], step=1)
    min_price = st.number_input('Min Price ($)', value=fields_options['min_price'], step=1)
    max_price = st.number_input('Max Price ($)', value=fields_options['max_price'], step=1)

    return {
        'operation': operation,
        'type': property_type,
        'state': state,
        'city': city,
        'neighborhood': neighborhood,
        'dorms': dorms,
        'toilets': toilets,
        'garages': garages,
        'min_size': min_size,
        'max_size': max_size,
        'min_price': min_price,
        'max_price': max_price
    }

def render_report(filters):
    # Get Report #
    (summary_by_type, type_distribution, summary_by_location,
     location_plots, clusters_map, price_heatmap, report_summary) = get_report(filters)

    # Store report data in session state
    st.session_state['report_data'] = filters

    # Report Summary #
    st.markdown("---")
    st.subheader('Report Summary')
    st.table(report_summary)

    # Summary by Type Table #
    st.subheader("Summary by Property Type")
    st.dataframe(summary_by_type.style.format(
        {"size": "{:,.2f}", "dorms": "{:,.2f}", "toilets": "{:,.2f}", "garage": "{:,.2f}", "price": "{:,.2f}",
         "additional_costs": "{:,.2f}", "price_per_sqm": "{:,.2f}"}))

    # Type Distribution Pie Chart #
    st.subheader("Type Distribution")
    st.pyplot(type_distribution)

    # Summary by Location Table #
    st.subheader("Summary by Location")
    st.dataframe(summary_by_location.style.format(
        {"Price/sqm": "{:,.2f}", "Price": "{:,.2f}", "Count": "{:,.0f}", "Size": "{:,.2f}",
         "Additional costs": "{:,.2f}", "Dorms": "{:,.2f}", "Toilets": "{:,.2f}", "Garages": "{:,.2f}",
         "Apartment ratio": "{:,.2%}", "House ratio": "{:,.2%}"}))

    # Locations Plots #
    st.subheader("Location Plots")
    st.pyplot(location_plots)

    # Clusters Map #
    st.subheader("Clusters Map")
    folium_static(clusters_map, width=700)

    # Price Heatmap #
    st.subheader("Price Heatmap")
    folium_static(price_heatmap, width=700)

def render_price_form():
    """Render the Price Predictor form."""
    st.subheader("Price Predictor")
    with st.form(key='price_predictor_form'):
        operation = st.selectbox("Operation (Selling or Renting)", ["selling", "renting"])
        size = st.number_input("Size (m2)", value=0, step=1)
        dorms = st.number_input("Number of Dorms", value=1, step=1)
        toilets = st.number_input("Number of Toilets", value=1, step=1)
        garages = st.number_input("Number of Garages", value=1, step=1)
        location = st.number_input("Location (Check clusters map)", value=0, step=1)
        property_type = st.selectbox("Type", ["Apartment", "House"])
        submit_button = st.form_submit_button("Predict Price")

        if submit_button:
            with st.spinner('Processing Prediction...'):
                st.session_state['predicted_price'] = {
                    'size': size,
                    'dorms': dorms,
                    'toilets': toilets,
                    'garage': garages,
                    'location': location,
                    'type': 1 if property_type == "Apartament" else 0,
                    'operation': operation
                }
                prediction = get_prediction(st.session_state['predicted_price'])
                st.subheader(f"Predicted Price: {prediction}")

def main():
    # Load initial options #
    fields_options = get_initial_options()

    # Check if a report has already been submitted #
    if 'report_data' in st.session_state:
        # Render the main form with initial options #
        filters = render_form(fields_options)

        # Check if button was pressed #
        if st.button('Submit New Report'):
            # Remove previous report data state #
            st.session_state.pop('report_data', None)

            # Render new report #
            with st.spinner('Processing Report...'):
                render_report(filters)
                render_price_form()
        # If not, render previous report #
        else:
            with st.spinner('Processing Report...'):
                render_report(st.session_state['report_data'])
                render_price_form()

    # First time on page #
    else:
        filters = render_form(fields_options)

        if st.button('Submit'):
            with st.spinner('Processing Report...'):
                render_report(filters)
                render_price_form()

if __name__ == '__main__':
    main()

