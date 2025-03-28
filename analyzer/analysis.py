import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from preprocessor import Preprocessor
import requests
import io
import base64
sns.set_theme()
pd.options.display.float_format = '{:,.2f}'.format

def run_analysis(filters):
    # Fetch data from database
    df = fetch_data(filters)
    
    # Preprocess data
    preprocessor, processed_df = preprocess_data(df)
    
    # Run analysis
    corr_matrix = correlation_matrix(processed_df)
    loc_plots = location_plots(processed_df)
    loc_summary = summarize_by_location(processed_df)
    type_summary = summarize_by_type(processed_df)
    type_dist = type_distribution(processed_df)
    
    # Return analysis
    return {
        "corr_matrix": corr_matrix.to_dict(),
        "loc_plots": loc_plots,
        "loc_summary": loc_summary.to_dict(),
        "type_summary": type_summary.to_dict(),
        "type_dist": type_dist,
        "clusters_map": preprocessor.clusters_map,
        "price_heatmap": preprocessor.price_heatmap
    } 

def fetch_data(filters):
    try:
        response = requests.post(f"http://api:8000/properties/filter", timeout=10, json=filters)
        response.raise_for_status() 
        data = response.json()

        # Convert to dataframe
        df = pd.DataFrame(data)
        
        # Return dataframe
        return df
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def preprocess_data(df):
    preprocessor = Preprocessor()
    processed_df = preprocessor.process_df(df)
    return preprocessor, processed_df

def fig_to_base64(fig):
    """Convert a Matplotlib figure to a Base64-encoded string."""
    img_io = io.BytesIO()
    fig.savefig(img_io, format='png', bbox_inches='tight')
    img_io.seek(0)
    base64_img = base64.b64encode(img_io.getvalue()).decode()
    plt.close(fig)
    return base64_img

def correlation_matrix(df, show=False):
    corr_matrix = df.corr()
    if show:
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
        plt.title("Correlation Matrix")
        plt.show()
        
    return corr_matrix

def location_plots(df):
    """Plots size, dorms, toilets, garage, additional costs, and type per location."""
    fig, axes = plt.subplots(3, 2, figsize=(9, 8))

    sns.boxplot(data=df, x='location', y='size', ax=axes[0, 0])
    axes[0, 0].set_title('Size per Location')

    sns.boxplot(data=df, x='location', y='dorms', ax=axes[0, 1])
    axes[0, 1].set_title('Dorms per Location')

    sns.boxplot(data=df, x='location', y='toilets', ax=axes[1, 0])
    axes[1, 0].set_title('Toilets per Location')

    sns.boxplot(data=df, x='location', y='garage', ax=axes[1, 1])
    axes[1, 1].set_title('Garage per Location')

    sns.countplot(data=df, x='location', hue='type', ax=axes[2, 0])
    axes[2, 0].set_title('Type Distribution per Location')

    plt.tight_layout()

    return fig_to_base64(fig)

def summarize_by_type(df):
    """ Create a summary by type table. """
    summary = df.groupby('type').agg({
        'size': 'mean',
        'dorms': 'mean',
        'toilets': 'mean',
        'garage': 'mean',
        'price': 'mean',
        'additional_costs': 'mean',
        'price_per_sqm': 'mean'
    }).reset_index()

    # Rename columns for clarity
    summary['type'] = summary['type'].map({1: 'Apartment', 0: 'House'})

    return summary

def type_distribution(df):
    """ Create a type distribution pie chart. """
    type_counts = df['type'].value_counts()
    type_counts.index = type_counts.index.map({1: 'Apartment', 0: 'House'})

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=90)
    ax.set_title('Type Distribution')
    return fig_to_base64(fig)

def summarize_by_location(df):
    """ Create a simplified summary by location. """

    # Aggregation and grouping by location
    summary = df.groupby('location').agg({
        'price_per_sqm': 'mean',
        'price': 'mean',
        'size': ['count', 'mean'],
        'type': lambda x: x.value_counts(normalize=True).to_dict(),
        'additional_costs': 'mean',
        'dorms': 'mean',
        'toilets': 'mean',
        'garage': 'mean'
    }).reset_index()

    # Flattening multi-level columns
    summary.columns = ['Location', 'Price/sqm', 'Price', 'Count', 'Size',
                        'type_distribution', 'Additional costs', 'Dorms', 'Toilets', 'Garages']

    # Splitting the 'type' distribution into two columns: Apartment and House
    summary['Apartment ratio'] = summary['type_distribution'].apply(lambda x: x.get(1, 0))
    summary['House ratio'] = summary['type_distribution'].apply(lambda x: x.get(0, 0))

    # Dropping the original 'type_distribution' column
    summary.drop(columns=['type_distribution'], inplace=True)

    return summary