import React, { useState, useEffect } from 'react';
import SelectionField from './SelectionField.js';
import './PricePredictionForm.css';

const LoadingOverlay = () => (
    <div className="loading-overlay">
        <div className="loading-spinner">
        </div>
        <div className="loading-text">
            Loading your data, it will take just a few seconds...
        </div>
    </div>
);

const MapModal = ({ mapHtml, onClose }) => (
    <div className="map-modal-overlay">
        <div className="map-modal-content">
            <button className="map-modal-close" onClick={onClose}>×</button>
            <div className="map-description">
                <h3>Location Clusters Visualization</h3>
                <p>
                    This map displays the geographical distribution of properties used in our model training.
                    Each color represents a different location cluster, which groups properties with similar
                    geographical characteristics. These clusters help us understand how location impacts
                    property values in different areas of the city.
                </p>
            </div>
            <div className="map-container" dangerouslySetInnerHTML={{ __html: mapHtml }} />
        </div>
    </div>
);

const PricePredictionForm = () => {
    const [isLoading, setIsLoading] = useState(true);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [showMap, setShowMap] = useState(false);
    const [canSubmit, setCanSubmit] = useState(false);
    const [options, setOptions] = useState([]);
    const [availableOperations, setAvailableOperations] = useState([]);
    const [availableLocations, setAvailableLocations] = useState([]);
    const [availableTypes] = useState([
        { label: 'Apartment', value: 1 },
        { label: 'House', value: 0 }
    ]);
    const [formData, setFormData] = useState({
        operation: '',
        type: availableTypes[0].value,
        location: '',
        size: '',
        dorms: '',
        toilets: '',
        garage: '',
        map: ''
    });

    // Fetch models options
    useEffect(() => {
        setIsLoading(true);
        fetch('http://localhost:8000/price-models')
            .then(response => response.json())
            .then(data => {
                const options = data.map(option => ({
                    operation: option.operation,
                    locations: option.k_clusters,
                    map: option.clusters_map,
                }));
                setOptions(options);

                // Set available operations
                const operations = options.map(opt => ({
                    label: opt.operation.charAt(0).toUpperCase() + opt.operation.slice(1),
                    value: opt.operation
                }));
                setAvailableOperations(operations);

                // Set initial operation and location if options exist
                if (options.length > 0) {
                    const firstOperation = options[0];
                    const initialLocations = Array.from({ length: firstOperation.locations }, (_, i) => ({
                        label: `Location ${i}`,
                        value: i.toString()
                    }));

                    setAvailableLocations(initialLocations);
                    setFormData(prev => ({
                        ...prev,
                        operation: firstOperation.operation,
                        location: '0', // Set first location
                        map: firstOperation.map
                    }));
                }
            })
            .finally(() => setIsLoading(false));
    }, []);

    // Update available locations when operation changes
    useEffect(() => {
        if (formData.operation) {
            const selectedOption = options.find(opt => opt.operation === formData.operation);
            if (selectedOption) {
                // Generate location options based on k_clusters
                const locations = Array.from({ length: selectedOption.locations }, (_, i) => ({
                    label: `Location ${i}`,
                    value: i.toString()
                }));
                setAvailableLocations(locations);
                // Update map in formData
                setFormData(prev => ({
                    ...prev,
                    map: selectedOption.map
                }));
            }
        } else {
            setAvailableLocations([]);
        }
    }, [formData.operation, options]);

    const validateForm = (data) => {
        return (
            data.operation !== '' &&
            data.type !== '' &&
            data.location !== '' &&
            data.size !== '' &&
            data.dorms !== '' &&
            data.toilets !== '' &&
            data.garage !== '' &&
            data.map !== ''
        );
    };

    useEffect(() => {
        setCanSubmit(validateForm(formData));
    }, [formData]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setIsSubmitting(true);
        // TODO: Implement API call to backend for price prediction
        console.log('Form submitted:', formData);
        // Simulate API call
        setTimeout(() => {
            setIsSubmitting(false);
        }, 2000);
    };

    const handleShowMap = () => {
        setShowMap(true);
    };

    const handleCloseMap = () => {
        setShowMap(false);
    };

    return (
        <div className="form-container">
            {isLoading && <LoadingOverlay />}
            {isSubmitting && <LoadingOverlay />}
            {showMap && <MapModal mapHtml={formData.map} onClose={handleCloseMap} />}

            <form onSubmit={handleSubmit} className="prediction-form">
                {/* Row 1: Operation and Type */}
                <div className="form-row">
                    <SelectionField
                        id="operation"
                        name="operation"
                        title="Select Operation"
                        options={availableOperations}
                        selectedValue={formData.operation}
                        onChange={handleChange}
                        required={true}
                    />

                    <SelectionField
                        id="type"
                        name="type"
                        title="Select Property Type"
                        options={availableTypes}
                        selectedValue={formData.type}
                        onChange={handleChange}
                        required={true}
                    />
                </div>

                {/* Row 2: Location */}
                <div className="form-row">
                    <div className="location-container">
                        <SelectionField
                            id="location"
                            name="location"
                            title="Select Location"
                            options={availableLocations}
                            selectedValue={formData.location}
                            onChange={handleChange}
                            required={true}
                        />
                        <button
                            type="button"
                            className="map-button"
                            onClick={handleShowMap}
                            disabled={!formData.operation}
                        >
                            Check Location Map
                        </button>
                    </div>
                </div>

                {/* Row 3: Size, Bedrooms, Bathrooms, Garage */}
                <div className="form-row">
                    <div className="form-group required">
                        <label className="required">Size (m²)</label>
                        <input
                            type="number"
                            id="size"
                            name="size"
                            value={formData.size}
                            onChange={handleChange}
                            min="0"
                            placeholder="Enter size"
                            required
                        />
                    </div>

                    <div className="form-group required">
                        <label className="required">Bedrooms</label>
                        <input
                            type="number"
                            id="dorms"
                            name="dorms"
                            value={formData.dorms}
                            onChange={handleChange}
                            min="0"
                            placeholder="Number of bedrooms"
                            required
                        />
                    </div>

                    <div className="form-group required">
                        <label className="required">Bathrooms</label>
                        <input
                            type="number"
                            id="toilets"
                            name="toilets"
                            value={formData.toilets}
                            onChange={handleChange}
                            min="0"
                            placeholder="Number of bathrooms"
                            required
                        />
                    </div>

                    <div className="form-group required">
                        <label className="required">Garage Spaces</label>
                        <input
                            type="number"
                            id="garage"
                            name="garage"
                            value={formData.garage}
                            onChange={handleChange}
                            min="0"
                            placeholder="Number of garage spaces"
                            required
                        />
                    </div>
                </div>

                <button type="submit" className={`submit-button ${!canSubmit ? 'disabled' : ''}`} disabled={!canSubmit}>
                    Predict Price
                </button>
            </form>
        </div>
    );
};

export default PricePredictionForm;