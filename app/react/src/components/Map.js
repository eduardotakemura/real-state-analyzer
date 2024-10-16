import React from 'react';

const Map = ({ mapData }) => {
    return (
         <div className="report-content">
            {mapData ? (
                <div dangerouslySetInnerHTML={{ __html: mapData }} />
            ) : (
                <p>No clusters map available</p>
            )}
        </div>
        )
};

export default Map;