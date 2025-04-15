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
    print("Data fetched: ", df.shape)

    # Preprocess data
    preprocessor, processed_df = preprocess_data(df)
    print("Data processed: ", processed_df.shape)

    # Run analysis
    plots = generate_plots(processed_df)
    loc_summary = summarize_by_location(processed_df)
    
    # Return analysis
    return {
        "plots": plots,
        "loc_summary": loc_summary.to_dict(),
        "clusters_map": preprocessor.clusters_map,
        "price_heatmap": preprocessor.price_heatmap,
        "operation": filters['operation'],
        "entries_count": len(processed_df)
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

def generate_plots(df):
    """Creates a 2x2 grid of location-based real estate plots with styled visuals."""
    # Copy and map 'type' to readable strings
    type_map = {0: 'House', 1: 'Apartment'}
    df = df.copy()
    df['type'] = df['type'].map(type_map)

    # Add price per square meter column
    df['price_per_sqm'] = df['price'] / df['size']

    # Define vivid color palette
    vivid_palette = ['#007acc', '#ff6600']
    box_palette = ['#4dabf7'] * df['location'].nunique()

    # Set style
    sns.set_style("whitegrid")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # --- 1. Size per Location (boxplot)
    sns.boxplot(data=df, x='location', y='size', ax=axes[0, 0], palette=box_palette)
    axes[0, 0].set_title('Property Size by Location')
    axes[0, 0].set_xlabel('Location')
    axes[0, 0].set_ylabel('Size (m²)')
    axes[0, 0].tick_params(axis='x', rotation=0)
    axes[0, 0].set_yticks(range(0, int(df['size'].max()) + 50, 50))

    # --- 2. Price per sqm by Location (boxplot)
    sns.boxplot(data=df, x='location', y='price_per_sqm', ax=axes[0, 1], palette=box_palette)
    axes[0, 1].set_title('Price per m² by Location (R$/m²)')
    axes[0, 1].set_xlabel('Location')
    axes[0, 1].set_ylabel('Price per m² (R$)')
    axes[0, 1].tick_params(axis='x', rotation=0)
    step = 3000 if df['price_per_sqm'].max() > 1000 else 50
    axes[0, 1].set_yticks(range(0, int(df['price_per_sqm'].max()) + step, step))

    # --- 3. Type Percentage per Location (stacked bar)
    type_loc = df.groupby(['location', 'type']).size().unstack().fillna(0)
    type_percent = (type_loc.T / type_loc.T.sum()).T * 100
    type_percent.plot(
        kind='bar',
        stacked=True,
        ax=axes[1, 0],
        color=vivid_palette,
        edgecolor='black'
    )
    axes[1, 0].set_ylabel('Percentage (%)')
    axes[1, 0].set_title('Type (%) by Location')
    axes[1, 0].set_xlabel('Location')
    axes[1, 0].legend(title='Type')
    axes[1, 0].tick_params(axis='x', rotation=0)

    # --- 4. Overall Type Distribution (pie chart)
    type_counts = df['type'].value_counts()
    axes[1, 1].pie(
        type_counts,
        labels=type_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=vivid_palette,
        wedgeprops={'edgecolor': 'white'}
    )
    axes[1, 1].set_title('Overall Type Distribution')
    axes[1, 1].axis('equal')

    plt.tight_layout()
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