import React from 'react';

const Figure = ({ figure, width, alt }) => {
    return (
        <div className="figure-container" style={{ width: `${width}%` }}>
            <img className="chart-image" src={`data:image/png;base64,${figure}`} alt={alt} />
        </div>
        )
};

export default Figure;