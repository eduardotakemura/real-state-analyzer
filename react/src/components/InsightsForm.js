import React, { useState, useEffect } from 'react';
import SelectionField from './SelectionField.js';
import AnalysisReport from './AnalysisReport.js';
import './InsightsForm.css';
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

const InsightsForm = () => {
    const [isLoading, setIsLoading] = useState(true);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [showAllFields, setShowAllFields] = useState(false);
    const [showReport, setShowReport] = useState(false);
    const [analysisData, setAnalysisData] = useState(null);
    const [formData, setFormData] = useState({
        operation: '',
        type: '',
        city: '',
        neighborhood: '',
        dorms: '',
        toilets: '',
        garage: '',
        min_size: '0',
        max_size: '0',
        min_price: '0',
        max_price: '0'
    });

    const [options, setOptions] = useState({
        count: 0,
        operations: [],
        types: [],
        cities: [],
        neighborhoods: [],
        max_size: 0,
        min_size: 0,
        max_price: 0,
        min_price: 0
    });

    // WebSocket connection
    useEffect(() => {
        const socket = new WebSocket(`${API_URL}/ws-insights`);

        socket.onopen = () => {
            console.log('Analyzer WebSocket connection established');
        };

        socket.onmessage = (event) => {
            try {
                // Replace NaN values with null before parsing
                const sanitizedData = event.data.replace(/:NaN/g, ':null');
                const message = JSON.parse(sanitizedData);
                console.log("Received Analyzer WebSocket message:", message);

                if (message.type === 'analysis') {
                    console.log("Analysis data received:", message.data);
                    // Convert null back to NaN for numeric fields
                    const processedData = processAnalysisData(message.data);
                    setAnalysisData(processedData);
                    setShowReport(true);
                    setIsSubmitting(false);
                }
            } catch (error) {
                console.error("Error parsing Analyzer WebSocket message:", error);
            }
        };

        socket.onerror = (error) => {
            console.error("Analyzer WebSocket error:", error);
        };

        socket.onclose = () => {
            console.log("Analyzer WebSocket connection closed");
        };

        return () => socket.close();
    }, []);

    const processAnalysisData = (data) => {
        // Helper function to recursively process the data and convert null back to NaN
        const processValue = (value) => {
            if (value === null) return NaN;
            if (typeof value === 'object' && value !== null) {
                if (Array.isArray(value)) {
                    return value.map(processValue);
                }
                const processed = {};
                for (const key in value) {
                    processed[key] = processValue(value[key]);
                }
                return processed;
            }
            return value;
        };

        return processValue(data);
    };

    // Fetch initial options
    useEffect(() => {
        fetch(`${API_URL}/properties/initial-options`)
            .then(response => response.json())
            .then(data =>
                setOptions({
                    count: data.count,
                    operations: data.operations,
                    types: [],
                    cities: [],
                    neighborhoods: [],
                    min_size: 0,
                    max_size: 0,
                    min_price: 0,
                    max_price: 0
                })
            )
            .finally(() => setIsLoading(false));
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleOperationChange = (e) => {
        const selectedOperation = e.target.value;

        // Update operation in form data
        setFormData(prev => ({
            ...prev,
            operation: selectedOperation,
            type: '', // Reset to "All" when operation changes
            city: '', // Reset to "All" when operation changes
            neighborhood: '' // Reset to "All" when operation changes
        }));

        if (selectedOperation) {
            setIsLoading(true);
            setShowAllFields(true);

            // Fetch options for operation
            fetch(`${API_URL}/properties/options/${selectedOperation}`)
                .then(response => response.json())
                .then(data => {
                    setOptions(prev => ({
                        ...prev,
                        count: data.count,
                        operations: prev.operations,
                        types: data.types,
                        cities: data.cities,
                        neighborhoods: data.neighborhoods,
                        min_size: data.min_size,
                        max_size: data.max_size,
                        min_price: data.min_price,
                        max_price: data.max_price
                    }));

                    // Reset range values to min/max
                    setFormData(prev => ({
                        ...prev,
                        min_size: data.min_size,
                        max_size: data.max_size,
                        min_price: data.min_price,
                        max_price: data.max_price
                    }));
                })
                .finally(() => setIsLoading(false));
        } else {
            setShowAllFields(false);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setIsSubmitting(true);
        setShowReport(false);

        fetch(`${API_URL}/request-analysis`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
            .catch(error => {
                console.error('Error submitting form:', error);
                setIsSubmitting(false);
            });
    };

    const handleReset = () => {
        setShowReport(false);
        setAnalysisData(null);
    };

    return (
        <div className="form-container">
            {isLoading && <LoadingOverlay />}
            {isSubmitting && <LoadingOverlay />}

            {!showReport ? (
                <form onSubmit={handleSubmit} className="insights-form">
                    <div className="form-description">
                        <p>Use the following form to get insights about the property you want to sell or rent,
                            apply filters to refine your search and get more accurate results.</p>
                    </div>
                    <SelectionField
                        id="operation"
                        title="Select Desired Operation (Selling/Renting)"
                        options={[
                            { value: '', label: 'Select Operation' },
                            ...options.operations.map(operation => ({
                                value: operation,
                                label: operation.charAt(0).toUpperCase() + operation.slice(1)
                            }))
                        ]}
                        selectedValue={formData.operation}
                        onChange={handleOperationChange}
                        required={true}
                    />

                    {showAllFields && (
                        <>
                            {/* Row 2: Type, City and Neighborhood */}
                            <div className="form-row">
                                <SelectionField
                                    id="type"
                                    title="Select Property Type"
                                    options={[
                                        { value: '', label: 'All Types' },
                                        ...options.types.map(type => ({ value: type, label: type }))
                                    ]}
                                    selectedValue={formData.type}
                                    onChange={handleChange}
                                />

                                <SelectionField
                                    id="city"
                                    title="Select City"
                                    options={[
                                        { value: '', label: 'All Cities' },
                                        ...options.cities.map(city => ({ value: city, label: city }))
                                    ]}
                                    selectedValue={formData.city}
                                    onChange={handleChange}
                                />

                                <SelectionField
                                    id="neighborhood"
                                    title="Select Neighborhood"
                                    options={[
                                        { value: '', label: 'All Neighborhoods' },
                                        ...options.neighborhoods.map(neighborhood => ({ value: neighborhood, label: neighborhood }))
                                    ]}
                                    selectedValue={formData.neighborhood}
                                    onChange={handleChange}
                                />
                            </div>

                            {/* Row 3: Bedrooms, Bathrooms, Garage */}
                            <div className="form-row">
                                <SelectionField
                                    id="dorms"
                                    title="Number of Bedrooms"
                                    options={[{ value: "", label: 'Any' }, { value: 1, label: '1+' }, { value: 2, label: '2+' }, { value: 3, label: '3+' }]}
                                    selectedValue={formData.dorms}
                                    onChange={handleChange}
                                />

                                <SelectionField
                                    id="toilets"
                                    title="Number of Bathrooms"
                                    options={[{ value: "", label: 'Any' }, { value: 1, label: '1+' }, { value: 2, label: '2+' }, { value: 3, label: '3+' }]}
                                    selectedValue={formData.toilets}
                                    onChange={handleChange}
                                />

                                <SelectionField
                                    id="garage"
                                    title="Garage Spaces"
                                    options={[{ value: "", label: 'Any' }, { value: 1, label: '1+' }, { value: 2, label: '2+' }, { value: 3, label: '3+' }]}
                                    selectedValue={formData.garage}
                                    onChange={handleChange}
                                />
                            </div>

                            {/* Row 4: Size and Price Range */}
                            <div className="form-row">
                                <div className="form-group">
                                    <label>Size Range (m²)</label>
                                    <div className="range-container">
                                        <input
                                            type="range"
                                            id="min_size"
                                            name="min_size"
                                            value={formData.min_size}
                                            onChange={handleChange}
                                            min={options.min_size}
                                            max={options.max_size}
                                            step="20"
                                        />
                                        <span className="range-value">{formData.min_size} m²</span>
                                    </div>
                                    <div className="range-container">
                                        <input
                                            type="range"
                                            id="maxSize"
                                            name="max_size"
                                            value={formData.max_size}
                                            onChange={handleChange}
                                            min={options.min_size}
                                            max={options.max_size}
                                            step="20"
                                        />
                                        <span className="range-value">{formData.max_size} m²</span>
                                    </div>
                                </div>

                                <div className="form-group">
                                    <label>Price Range</label>
                                    <div className="range-container">
                                        <input
                                            type="range"
                                            id="min_price"
                                            name="min_price"
                                            value={formData.min_price}
                                            onChange={handleChange}
                                            min={options.min_price}
                                            max={options.max_price}
                                            step="10000"
                                        />
                                        <span className="range-value">R${formData.min_price}</span>
                                    </div>
                                    <div className="range-container">
                                        <input
                                            type="range"
                                            id="max_price"
                                            name="max_price"
                                            value={formData.max_price}
                                            onChange={handleChange}
                                            min={options.min_price}
                                            max={options.max_price}
                                            step="10000"
                                        />
                                        <span className="range-value">R${formData.max_price}</span>
                                    </div>
                                </div>
                            </div>

                            <button type="submit" className={`submit-button ${formData.operation === '' ? 'disabled' : ''}`}>
                                Get Insights
                            </button>
                        </>
                    )}
                </form>
            ) : (
                <div className="report-container">
                    <button onClick={handleReset} className="reset-button">
                        Back to Search
                    </button>
                    <AnalysisReport data={analysisData} />
                </div>
            )}
        </div>
    );
};

export default InsightsForm; 