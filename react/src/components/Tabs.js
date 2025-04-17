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
            <button
                className={`tab ${activeTab === 'api' ? 'active' : ''}`}
                onClick={() => setActiveTab('api')}
            >
                API
            </button>
        </div>
    );
};

export default Tabs; 