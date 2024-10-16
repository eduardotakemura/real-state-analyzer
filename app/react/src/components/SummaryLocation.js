import React from 'react';

const SummaryLocation = ({ summary }) => {
    return (<table className="summary-table">
                <thead>
                    <tr>
                        <th>Location</th>
                        <th>Price/sqm</th>
                        <th>Price</th>
                        <th>Count</th>
                        <th>Size</th>
                        <th>Apartment Ratio</th>
                        <th>House Ratio</th>
                        <th>Additional Costs</th>
                        <th>Dorms</th>
                        <th>Toilets</th>
                        <th>Garages</th>
                    </tr>
                </thead>
                <tbody>
                    {summary.map((row, index) => (
                        <tr key={index}>
                            <td>{row.Location}</td>
                            <td>{row['Price/sqm'].toFixed(2)}</td>
                            <td>{row.Price.toFixed(2)}</td>
                            <td>{row.Count}</td>
                            <td>{row.Size.toFixed(2)}</td>
                            <td>{(row['Apartment ratio'] * 100).toFixed(2)}%</td>
                            <td>{(row['House ratio'] * 100).toFixed(2)}%</td>
                            <td>{row['Additional costs'].toFixed(2)}</td>
                            <td>{row.Dorms.toFixed(2)}</td>
                            <td>{row.Toilets.toFixed(2)}</td>
                            <td>{row.Garages.toFixed(2)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>)
};
export default SummaryLocation;