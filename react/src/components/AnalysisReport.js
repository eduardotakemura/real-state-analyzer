import React, { useState, useEffect } from 'react';
import './AnalysisReport.css';

const AnalysisReport = ({ data }) => {
    const [visibleComponents, setVisibleComponents] = useState({
        summary: false,
        clustersMap: false,
        locSummary: false,
        plots: false,
        priceHeatmap: false,
        operation: false,
        entriesCount: false
    });

    useEffect(() => {
        // Show components in sequence with delays
        const delays = {
            summary: 0,
            clustersMap: 200,
            locSummary: 400,
            plots: 600,
            priceHeatmap: 800
        };

        Object.entries(delays).forEach(([component, delay]) => {
            setTimeout(() => {
                setVisibleComponents(prev => ({
                    ...prev,
                    [component]: true
                }));
            }, delay);
        });
    }, []);

    const formatNumber = (value) => {
        if (typeof value !== 'number') return value;
        return value.toLocaleString('de-DE');
    };

    const renderSummary = () => {
        return (
            <div className={`report-section ${visibleComponents.summary ? 'visible' : ''}`}>
                <h3 className="section-title">Analysis Summary</h3>
                <div className="summary-box">
                    <div className="summary-item">
                        <span className="summary-label">Operation:</span>
                        <span className="summary-value">{data.operation}</span>
                    </div>
                    <div className="summary-item">
                        <span className="summary-label">Total Properties:</span>
                        <span className="summary-value">{formatNumber(data.entries_count)}</span>
                    </div>
                </div>
            </div>
        );
    };

    const renderLocationSummary = () => {
        const summary = data.loc_summary;
        const columns = Object.keys(summary);

        // Filter out unwanted columns
        const displayColumns = columns.filter(col =>
            !['Dorms', 'Toilets', 'Garages', 'Count'].includes(col)
        );

        return (
            <div className={`report-section ${visibleComponents.locSummary ? 'visible' : ''}`}>
                <h3 className="section-title">Location Summary</h3>
                <p className="section-subtitle">Detailed statistics for each location cluster</p>
                <table className="summary-table">
                    <thead>
                        <tr>
                            {displayColumns.map(col => {
                                const titles = {
                                    'Location': 'Location',
                                    'Price/sqm': 'Price/m²',
                                    'Price': 'Average price',
                                    'Size': 'Average size (m²)',
                                    'Additional costs': 'Average additional costs',
                                    'Apartment ratio': 'Apartment ratio (%)',
                                    'House ratio': 'House ratio (%)'
                                };
                                return <th key={col}>{titles[col] || col}</th>;
                            })}
                        </tr>
                    </thead>
                    <tbody>
                        {Object.keys(summary[columns[0]]).map(location => (
                            <tr key={location}>
                                {displayColumns.map(col => {
                                    const value = summary[col][location];
                                    if (typeof value === 'number') {
                                        if (col === 'Apartment ratio' || col === 'House ratio') {
                                            return (
                                                <td key={`${location}-${col}`}>
                                                    {(value * 100).toFixed(0)}%
                                                </td>
                                            );
                                        }
                                        return (
                                            <td key={`${location}-${col}`}>
                                                {formatNumber(Math.round(value))}
                                            </td>
                                        );
                                    }
                                    return (
                                        <td key={`${location}-${col}`}>
                                            {value}
                                        </td>
                                    );
                                })}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        );
    };

    return (
        <div className="analysis-report">
            {renderSummary()}
            <div
                className={`report-section ${visibleComponents.clustersMap ? 'visible' : ''}`}
            >
                <h3 className="section-title">Location Clusters</h3>
                <p className="section-subtitle">Geographic distribution of property clusters.</p>
                <p className="section-subtitle">Navigate through the map to explore the location distribution.</p>
                <div dangerouslySetInnerHTML={{ __html: data.clusters_map }} />
            </div>

            {renderLocationSummary()}

            <div className={`report-section ${visibleComponents.plots ? 'visible' : ''}`}>
                <h3 className="section-title">Location Analysis</h3>
                <p className="section-subtitle">Visual analysis of property distribution and characteristics</p>
                <img
                    src={`data:image/png;base64,${data.plots}`}
                    alt="Location Analysis Plots"
                    className="analysis-image"
                />
            </div>

            <div
                className={`report-section ${visibleComponents.priceHeatmap ? 'visible' : ''}`}
            >
                <h3 className="section-title">Price Distribution</h3>
                <p className="section-subtitle">Heatmap showing price distribution across locations</p>
                <div dangerouslySetInnerHTML={{ __html: data.price_heatmap }} />
            </div>
        </div>
    );
};

export default AnalysisReport; 