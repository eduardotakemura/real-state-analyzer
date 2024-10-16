import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
pd.options.display.float_format = '{:,.2f}'.format

class Analyzer:
    def __init__(self):
        pass

    def correlation_matrix(self, df, show=True):
        corr_matrix = df.corr()
        if show:
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
            plt.title("Correlation Matrix")
            plt.show()
        return corr_matrix

    def location_plots(self, df):
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

        return fig

    def summarize_by_type(self, df):
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

    def type_distribution(self, df):
        """ Create a type distribution pie chart. """
        type_counts = df['type'].value_counts()
        type_counts.index = type_counts.index.map({1: 'Apartment', 0: 'House'})

        fig, ax = plt.subplots(figsize=(4, 3))
        ax.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=90)
        ax.set_title('Type Distribution')
        return fig

    def summarize_by_location(self, df):
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