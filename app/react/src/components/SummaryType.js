import React from 'react';

const SummaryType = ({ summary }) => {
    return (<div className="summary-type-container">
                <table className="summary-table">
                    <thead>
                        <tr>
                            <th>Type</th>
                            <th>Size</th>
                            <th>Dorms</th>
                            <th>Toilets</th>
                            <th>Garage</th>
                            <th>Price</th>
                            <th>Additional Costs</th>
                            <th>Price per Sqm</th>
                        </tr>
                    </thead>
                    <tbody>
                        {summary.map((row, index) => (
                            <tr key={index}>
                                <td>{row.type}</td>
                                <td>{row.size.toFixed(2)}</td>
                                <td>{row.dorms.toFixed(2)}</td>
                                <td>{row.toilets.toFixed(2)}</td>
                                <td>{row.garage.toFixed(2)}</td>
                                <td>{row.price.toFixed(2)}</td>
                                <td>{row.additional_costs.toFixed(2)}</td>
                                <td>{row.price_per_sqm.toFixed(2)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>)
};

export default SummaryType;

