import React, { useState, useEffect } from 'react';
import SelectionField from './SelectionField.js';
import './PricePredictionForm.css';

const PricePredictionForm = () => {
    const [canSubmit, setCanSubmit] = useState(false);
    const [formData, setFormData] = useState({
        operation: 'selling',
        type: 1,
        location: '',
        size: '',
        dorms: '',
        toilets: '',
        garage: ''
    });

    const validateForm = (data) => {
        return (
            data.operation !== '' &&
            data.type !== '' &&
            data.location !== '' &&
            data.size !== '' &&
            data.dorms !== '' &&
            data.toilets !== '' &&
            data.garage !== ''
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
        // TODO: Implement API call to backend for price prediction
        console.log('Form submitted:', formData);
    };

    return (
        <form onSubmit={handleSubmit} className="prediction-form">
            {/* Row 1: Location */}
            <div className="form-row">
                <div className="form-group required">
                    <label className="required">Location</label>
                    <input
                        type="text"
                        id="location"
                        name="location"
                        value={formData.location}
                        onChange={handleChange}
                        placeholder="Enter property location"
                        className="location-input"
                    />
                </div>
            </div>

            {/* Row 2: Size, Bedrooms, Bathrooms, Garage */}
            <div className="form-row">
                <SelectionField
                    id="operation"
                    title="Select Desired Operation (Selling/Renting)"
                    options={[
                        { value: 'selling', label: 'Selling' },
                        { value: 'renting', label: 'Renting' }
                    ]}
                    selectedValue={formData.operation}
                    onChange={handleChange}
                    required={true}
                />

                <SelectionField
                    id="type"
                    title="Select Property Type"
                    options={[{ value: 1, label: 'Apartment' }, { value: 0, label: 'House' }]}
                    selectedValue={formData.type}
                    onChange={handleChange}
                    required={true}
                />
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

            <button type="submit" className={`submit-button ${canSubmit ? '' : 'disabled'}`} disabled={!canSubmit}>
                Predict Price
            </button>
        </form>
    );
};

export default PricePredictionForm; 