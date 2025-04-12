import React from 'react';
import './Tabs.css';

const Tabs = ({ activeTab, setActiveTab }) => {
    return (
        <div className="tabs">
            <button
                className={`tab ${activeTab === 'insights' ? 'active' : ''}`}
                onClick={() => setActiveTab('insights')}
            >
                Real Estate Insights
            </button>
            <button
                className={`tab ${activeTab === 'prediction' ? 'active' : ''}`}
                onClick={() => setActiveTab('prediction')}
            >
                Price Prediction
            </button>
        </div>
    );
};

export default Tabs; 