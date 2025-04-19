import React, { useState } from 'react';
import './ApiInterface.css';
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const LoadingOverlay = () => (
    <div className="loading-overlay">
        <div className="loading-spinner">
        </div>
        <div className="loading-text">
            Loading your data, it will take just a few seconds...
        </div>
    </div>
);

const ApiInterface = () => {
    const [loading, setLoading] = useState(false);
    const [selectedOperation, setSelectedOperation] = useState('selling');
    const [scrapingInput, setScrapingInput] = useState({
        url: '',
        pages: 1,
        file_name: '',
        date: new Date().toISOString().split('T')[0],
        tasks: ['scrape', 'preprocess', 'fetch_lat_lng', 'load']
    });
    const [results, setResults] = useState({
        export: null,
        training: null,
        scraping: null
    });

    const handleExport = async () => {
        setLoading(true);
        try {
            const response = await fetch(`${API_URL}/export-properties`)
                .then(response => {
                    if (response.ok) {
                        setResults({ ...results, export: 'Properties exported successfully.\nCheck the api/properties.csv file' });
                    } else {
                        setResults({ ...results, export: 'Export failed: ' + response.statusText });
                    }
                });

        } catch (error) {
            console.error('Export failed:', error);
            setResults({ ...results, export: 'Export failed: ' + error.message });
        }
        setLoading(false);
    };

    const handleTraining = async () => {
        setLoading(true);
        try {
            const response = await fetch(`${API_URL}/request-training`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ operation: selectedOperation })
            });
            const data = await response.json();
            console.log(data);
            setResults({ ...results, training: JSON.stringify(data, null, 2) });
        } catch (error) {
            console.error('Training request failed:', error);
            setResults({ ...results, training: 'Training failed: ' + error.message });
        }
        setLoading(false);
    };

    const handleScraping = async () => {
        setLoading(true);
        try {
            const selectedTasks = [];
            if (scrapingInput.tasks.includes('scrape')) selectedTasks.push('scrape');
            if (scrapingInput.tasks.includes('preprocess')) selectedTasks.push('preprocess');
            if (scrapingInput.tasks.includes('fetch_lat_lng')) selectedTasks.push('fetch_lat_lng');
            if (scrapingInput.tasks.includes('load')) selectedTasks.push('load');

            const task = {
                url: scrapingInput.url,
                pages: scrapingInput.pages,
                file_name: scrapingInput.file_name,
                operation: selectedOperation,
                date: scrapingInput.date,
                tasks: selectedTasks
            };

            const response = await fetch(`${API_URL}/request-scraping`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(task)
            });
            const data = await response.json();
            console.log(data);
            setResults({ ...results, scraping: JSON.stringify(data, null, 2) });
        } catch (error) {
            console.error('Scraping request failed:', error);
            setResults({ ...results, scraping: 'Scraping failed: ' + error.message });
        }
        setLoading(false);
    };

    const isScrapingFormValid = () => {
        return (
            scrapingInput.url.trim() !== '' &&
            scrapingInput.pages > 0 &&
            scrapingInput.file_name.trim() !== '' &&
            scrapingInput.tasks.length > 0
        );
    };

    return (
        <div className="api-interface">
            <h2>API Documentation</h2>

            <div className="api-section">
                <div className="api-header">
                    <div className="api-route">/export-properties</div>
                    <div className="api-description">Export all properties data to a CSV file</div>
                </div>
                <div className="api-actions">
                    <button onClick={handleExport} disabled={loading}>Request</button>
                    {results.export && (
                        <div className="result-box">
                            <pre>API Response: {results.export}</pre>
                        </div>
                    )}
                </div>
            </div>

            <div className="api-section">
                <div className="api-header">
                    <div className="api-route">/request-training</div>
                    <div className="api-description">Train the price prediction model for either selling or renting properties</div>
                </div>
                <div className="api-actions">
                    <div className="input-group">
                        <label>Operation Type</label>
                        <select
                            value={selectedOperation}
                            onChange={(e) => setSelectedOperation(e.target.value)}
                            disabled={loading}
                        >
                            <option value="selling">Selling</option>
                            <option value="renting">Renting</option>
                        </select>
                    </div>
                    <button onClick={handleTraining} disabled={loading}>Request</button>
                    {results.training && (
                        <div className="result-box">
                            <pre>API Response: {results.training}</pre>
                        </div>
                    )}
                </div>
            </div>

            <div className="api-section">
                <div className="api-header">
                    <div className="api-route">/request-scraping</div>
                    <div className="api-description">Scrape property data from the web, preprocess it, and optionally load it to the database</div>
                </div>
                <div className="api-actions">
                    <div className="input-group">
                        <label>URL</label>
                        <input
                            type="text"
                            placeholder="Enter the starting URL for scraping"
                            value={scrapingInput.url}
                            onChange={(e) => setScrapingInput({ ...scrapingInput, url: e.target.value })}
                            disabled={loading}
                        />
                    </div>
                    <div className="input-group">
                        <label>Number of Pages</label>
                        <input
                            type="number"
                            placeholder="How many pages to scrape"
                            value={scrapingInput.pages}
                            onChange={(e) => setScrapingInput({ ...scrapingInput, pages: parseInt(e.target.value) })}
                            disabled={loading}
                            min="1"
                        />
                    </div>
                    <div className="input-group">
                        <label>File Name</label>
                        <input
                            type="text"
                            placeholder="Name for the output file"
                            value={scrapingInput.file_name}
                            onChange={(e) => setScrapingInput({ ...scrapingInput, file_name: e.target.value })}
                            disabled={loading}
                        />
                    </div>
                    <div className="input-group">
                        <label>Operation Type</label>
                        <select
                            value={selectedOperation}
                            onChange={(e) => setSelectedOperation(e.target.value)}
                            disabled={loading}
                        >
                            <option value="selling">Selling</option>
                            <option value="renting">Renting</option>
                        </select>
                    </div>
                    <div className="input-group">
                        <label>Date</label>
                        <input
                            type="date"
                            value={scrapingInput.date}
                            onChange={(e) => setScrapingInput({ ...scrapingInput, date: e.target.value })}
                            disabled={loading}
                        />
                    </div>
                    <div className="checkbox-group">
                        <label>
                            <input
                                type="checkbox"
                                checked={scrapingInput.tasks.includes('scrape')}
                                onChange={(e) => {
                                    const tasks = e.target.checked
                                        ? [...scrapingInput.tasks, 'scrape']
                                        : scrapingInput.tasks.filter(task => task !== 'scrape');
                                    setScrapingInput({ ...scrapingInput, tasks });
                                }}
                                disabled={loading}
                            />
                            Scrape
                        </label>
                        <label>
                            <input
                                type="checkbox"
                                checked={scrapingInput.tasks.includes('preprocess')}
                                onChange={(e) => {
                                    const tasks = e.target.checked
                                        ? [...scrapingInput.tasks, 'preprocess']
                                        : scrapingInput.tasks.filter(task => task !== 'preprocess');
                                    setScrapingInput({ ...scrapingInput, tasks });
                                }}
                                disabled={loading}
                            />
                            Preprocess
                        </label>
                        <label>
                            <input
                                type="checkbox"
                                checked={scrapingInput.tasks.includes('fetch_lat_lng')}
                                onChange={(e) => {
                                    const tasks = e.target.checked
                                        ? [...scrapingInput.tasks, 'fetch_lat_lng']
                                        : scrapingInput.tasks.filter(task => task !== 'fetch_lat_lng');
                                    setScrapingInput({ ...scrapingInput, tasks });
                                }}
                                disabled={loading}
                            />
                            Fetch Lat/Lng
                        </label>
                        <label>
                            <input
                                type="checkbox"
                                checked={scrapingInput.tasks.includes('load')}
                                onChange={(e) => {
                                    const tasks = e.target.checked
                                        ? [...scrapingInput.tasks, 'load']
                                        : scrapingInput.tasks.filter(task => task !== 'load');
                                    setScrapingInput({ ...scrapingInput, tasks });
                                }}
                                disabled={loading}
                            />
                            Load to Database
                        </label>
                    </div>
                    <button
                        onClick={handleScraping}
                        disabled={loading || !isScrapingFormValid()}
                    >
                        Request
                    </button>
                    {results.scraping && (
                        <div className="result-box">
                            <pre>API Response: {results.scraping}</pre>
                        </div>
                    )}
                </div>
            </div>

            {loading && <LoadingOverlay />}
        </div>
    );
};

export default ApiInterface; 