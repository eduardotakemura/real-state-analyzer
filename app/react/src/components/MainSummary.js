import React from 'react';

const MainSummary = ({totalEntries,operation,locationsClusters}) => {
    return(
    <div className="main-summary">
        <h2>Report Summary</h2>
        <div className="summary-details">
            <p><strong>Effective Entries Processed:</strong> {totalEntries}</p>
            <p><strong>Reference Operation:</strong> {operation}</p>
            <p><strong>Locations Clusters Selected:</strong> {locationsClusters}</p>
        </div>
    </div>
    )
};

export default MainSummary;