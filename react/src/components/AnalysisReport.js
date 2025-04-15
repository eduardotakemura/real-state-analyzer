import React, { useState, useEffect } from 'react';
import './AnalysisReport.css';

const AnalysisReport = ({ data }) => {
    const [visibleComponents, setVisibleComponents] = useState({
        typeSummary: false,
        locSummary: false,
        corrMatrix: false,
        typeDist: false,
        locPlots: false,
        clustersMap: false,
        priceHeatmap: false
    });

    useEffect(() => {
        // Show components in sequence with delays
        const delays = {
            typeSummary: 0,
            locSummary: 200,
            corrMatrix: 400,
            typeDist: 600,
            locPlots: 800,
            clustersMap: 1000,
            priceHeatmap: 1200
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

    const renderCorrelationMatrix = () => {
        const matrix = data.corr_matrix;
        const columns = Object.keys(matrix);

        return (
            <div className={`report-section ${visibleComponents.corrMatrix ? 'visible' : ''}`}>
                <h3>Correlation Matrix</h3>
                <table className="correlation-table">
                    <thead>
                        <tr>
                            <th></th>
                            {columns.map(col => (
                                <th key={col}>{col}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {columns.map(row => (
                            <tr key={row}>
                                <th>{row}</th>
                                {columns.map(col => (
                                    <td key={`${row}-${col}`}>
                                        {matrix[row][col].toFixed(2)}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        );
    };

    const renderTypeSummary = () => {
        const summary = data.type_summary;
        const columns = Object.keys(summary);

        return (
            <div className={`report-section ${visibleComponents.typeSummary ? 'visible' : ''}`}>
                <h3>Property Type Summary</h3>
                <table className="summary-table">
                    <thead>
                        <tr>
                            {columns.map(col => (
                                <th key={col}>{col}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {Object.keys(summary[columns[0]]).map(type => (
                            <tr key={type}>
                                {columns.map(col => {
                                    const value = summary[col][type];
                                    // Handle numeric values
                                    if (typeof value === 'number') {
                                        return (
                                            <td key={`${type}-${col}`}>
                                                {isNaN(value) ? '-' : value.toFixed(2)}
                                            </td>
                                        );
                                    }
                                    // Handle other values
                                    return (
                                        <td key={`${type}-${col}`}>
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

    const renderLocationSummary = () => {
        const summary = data.loc_summary;
        const columns = Object.keys(summary);

        return (
            <div className={`report-section ${visibleComponents.locSummary ? 'visible' : ''}`}>
                <h3>Location Summary</h3>
                <table className="summary-table">
                    <thead>
                        <tr>
                            {columns.map(col => (
                                <th key={col}>{col}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {Object.keys(summary[columns[0]]).map(location => (
                            <tr key={location}>
                                {columns.map(col => {
                                    const value = summary[col][location];
                                    // Handle type_distribution object
                                    if (col === 'type_distribution') {
                                        return (
                                            <td key={`${location}-${col}`}>
                                                {`Apt: ${(value[1] * 100).toFixed(1)}%, House: ${(value[0] * 100).toFixed(1)}%`}
                                            </td>
                                        );
                                    }
                                    // Handle numeric values
                                    if (typeof value === 'number') {
                                        return (
                                            <td key={`${location}-${col}`}>
                                                {value.toFixed(2)}
                                            </td>
                                        );
                                    }
                                    // Handle other values
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
            {renderTypeSummary()}
            {renderLocationSummary()}
            {renderCorrelationMatrix()}

            <div className={`report-section ${visibleComponents.typeDist ? 'visible' : ''}`}>
                <h3>Property Type Distribution</h3>
                <img
                    src={`data:image/png;base64,${data.type_dist}`}
                    alt="Property Type Distribution"
                    className="analysis-image"
                />
            </div>

            <div className={`report-section ${visibleComponents.locPlots ? 'visible' : ''}`}>
                <h3>Location Analysis</h3>
                <img
                    src={`data:image/png;base64,${data.loc_plots}`}
                    alt="Location Analysis Plots"
                    className="analysis-image"
                />
            </div>

            <div
                className={`report-section ${visibleComponents.clustersMap ? 'visible' : ''}`}
                dangerouslySetInnerHTML={{ __html: data.clusters_map }}
            />

            <div
                className={`report-section ${visibleComponents.priceHeatmap ? 'visible' : ''}`}
                dangerouslySetInnerHTML={{ __html: data.price_heatmap }}
            />
        </div>
    );
};

export default AnalysisReport; 