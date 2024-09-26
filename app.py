import streamlit as st
from streamlit_folium import folium_static
from server import get_initial_options, get_report

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

def main():
    with st.spinner('Loading Dataset...'):
        # Fetch dropdown options from the backend #
        fields_options = get_initial_options()

        # Render form inputs and capture submitted filters #
        filters = render_form(fields_options)

    # Display Report #
    if st.button('Submit'):
        with st.spinner('Processing Report...'):
            render_report(filters)

if __name__ == '__main__':
    main()

