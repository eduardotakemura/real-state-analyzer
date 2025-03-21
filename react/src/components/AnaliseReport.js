import React from 'react';
import MainSummary from './MainSummary';
import SummaryType from './SummaryType';
import SummaryLocation from './SummaryLocation';
import Figure from './Figure';
import Map from './Map';

const AnaliseReport = ({ data }) => {
    const { total_entries, operation, locations_clusters, summary_by_type,
    type_distribution, summary_by_location, locations_plots, clusters_map,
    price_heatmap } = data;

    return (
        <div className="report">
            {/* Report Summary */}
            <MainSummary totalEntries={total_entries} operation={operation} locationsClusters={locations_clusters} />

            {/* Type Summary */}
            <div className="report-section">
                <h2 className="report-title">Summary by Type (Means)</h2>
                {/* Summary by Type Table */}
                <SummaryType summary={summary_by_type} />

                {/* Type Distribution Pie Chart */}
                <Figure figure={type_distribution} width={98} alt="Type Distribution Chart" />
            </div>

           {/* Location Summary */}
            <div className="report-section">
                <h2 className="report-title">Summary by Location (Means)</h2>
                {/* Summary by Location Table */}
                <SummaryLocation summary={summary_by_location} />

                {/* Locations plots */}
                <Figure figure={locations_plots} width={98} alt="Location Plots" />

            </div>

            {/* Maps */}
            <div className="report-section">
                <h2 className="report-title">Locations Clusters Map</h2>
                <Map mapData={clusters_map} />
            </div>
            <div className="report-section">
                <h2 className="report-title">Price Heatmap</h2>
                <Map mapData={price_heatmap} />
            </div>

        </div>
    );
};

export default AnaliseReport;
