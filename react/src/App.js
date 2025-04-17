import './App.css';
import React, { useState } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import Tabs from './components/Tabs';
import InsightsForm from './components/InsightsForm';
import PricePredictionForm from './components/PricePredictionForm';
import ApiInterface from './components/ApiInterface';

function App() {
    const [activeTab, setActiveTab] = useState('insights');

    return (
        <div className="App">
            <Header />

            <div className="container">
                <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />

                <div className="content">
                    {activeTab === 'insights' ? (
                        <InsightsForm />
                    ) : activeTab === 'prediction' ? (
                        <PricePredictionForm />
                    ) : (
                        <ApiInterface />
                    )}
                </div>
            </div>

            <Footer />
        </div>
    );
}

export default App;
