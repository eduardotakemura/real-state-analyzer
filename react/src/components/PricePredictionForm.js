import React, { useState } from 'react';
import './PricePredictionForm.css';

const PricePredictionForm = () => {
    const [formData, setFormData] = useState({
        location: '',
        size: '',
        dorms: '',
        toilets: '',
        garage: ''
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // TODO: Implement API call to backend for price prediction
        console.log('Form submitted:', formData);
    };

    return (
        <form onSubmit={handleSubmit} className="prediction-form">
            {/* Row 1: Location */}
            <div className="form-row">
                <div className="form-group location-input" style={{ width: '100%' }}>
                    <label htmlFor="location">Location</label>
                    <input
                        type="text"
                        id="location"
                        name="location"
                        value={formData.location}
                        onChange={handleChange}
                        placeholder="Enter location (will be used for API integration)"
                        required
                    />
                </div>
            </div>

            {/* Row 2: Size, Bedrooms, Bathrooms, Garage */}
            <div className="form-row">
                <div className="form-group" style={{ flex: 1 }}>
                    <label htmlFor="size">Size (m²)</label>
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

                <div className="form-group" style={{ flex: 1 }}>
                    <label htmlFor="dorms">Bedrooms</label>
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

                <div className="form-group" style={{ flex: 1 }}>
                    <label htmlFor="toilets">Bathrooms</label>
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

                <div className="form-group" style={{ flex: 1 }}>
                    <label htmlFor="garage">Garage Spaces</label>
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

            <button type="submit" className="submit-button">
                Predict Price
            </button>
        </form>
    );
};

export default PricePredictionForm; 