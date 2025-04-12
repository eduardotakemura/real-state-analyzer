import React, { useState } from 'react';
import './InsightsForm.css';

const InsightsForm = () => {
    const [formData, setFormData] = useState({
        operation: '',
        type: '',
        city: '',
        neighborhood: '',
        dorms: '',
        toilets: '',
        garage: '',
        minSize: '0',
        maxSize: '500',
        minPrice: '0',
        maxPrice: '1000000'
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
        // TODO: Implement API call to backend
        console.log('Form submitted:', formData);
    };

    return (
        <form onSubmit={handleSubmit} className="insights-form">
            {/* Row 1: Operation and Type */}
            <div className="form-row">
                <div className="form-group">
                    <label htmlFor="operation">Operation</label>
                    <select
                        id="operation"
                        name="operation"
                        value={formData.operation}
                        onChange={handleChange}
                    >
                        <option value="">Select Operation</option>
                        <option value="rent">Rent</option>
                        <option value="sale">Sale</option>
                    </select>
                </div>

                <div className="form-group">
                    <label htmlFor="type">Type</label>
                    <select
                        id="type"
                        name="type"
                        value={formData.type}
                        onChange={handleChange}
                    >
                        <option value="">Select Type</option>
                        <option value="apartment">Apartment</option>
                        <option value="house">House</option>
                        <option value="commercial">Commercial</option>
                    </select>
                </div>
            </div>

            {/* Row 2: City and Neighborhood */}
            <div className="form-row">
                <div className="form-group">
                    <label htmlFor="city">City</label>
                    <input
                        type="text"
                        id="city"
                        name="city"
                        value={formData.city}
                        onChange={handleChange}
                        placeholder="Enter city"
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="neighborhood">Neighborhood</label>
                    <input
                        type="text"
                        id="neighborhood"
                        name="neighborhood"
                        value={formData.neighborhood}
                        onChange={handleChange}
                        placeholder="Enter neighborhood"
                    />
                </div>
            </div>

            {/* Row 3: Bedrooms, Bathrooms, Garage */}
            <div className="form-row">
                <div className="form-group">
                    <label htmlFor="dorms">Bedrooms</label>
                    <input
                        type="number"
                        id="dorms"
                        name="dorms"
                        value={formData.dorms}
                        onChange={handleChange}
                        min="0"
                        placeholder="Number of bedrooms"
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="toilets">Bathrooms</label>
                    <input
                        type="number"
                        id="toilets"
                        name="toilets"
                        value={formData.toilets}
                        onChange={handleChange}
                        min="0"
                        placeholder="Number of bathrooms"
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="garage">Garage Spaces</label>
                    <input
                        type="number"
                        id="garage"
                        name="garage"
                        value={formData.garage}
                        onChange={handleChange}
                        min="0"
                        placeholder="Number of garage spaces"
                    />
                </div>
            </div>

            {/* Row 4: Size and Price Range */}
            <div className="form-row">
                <div className="form-group">
                    <label>Size Range (m²)</label>
                    <div className="range-container">
                        <input
                            type="range"
                            id="minSize"
                            name="minSize"
                            value={formData.minSize}
                            onChange={handleChange}
                            min="0"
                            max="500"
                            step="10"
                        />
                        <span className="range-value">{formData.minSize}m²</span>
                    </div>
                    <div className="range-container">
                        <input
                            type="range"
                            id="maxSize"
                            name="maxSize"
                            value={formData.maxSize}
                            onChange={handleChange}
                            min="0"
                            max="500"
                            step="10"
                        />
                        <span className="range-value">{formData.maxSize}m²</span>
                    </div>
                </div>

                <div className="form-group">
                    <label>Price Range</label>
                    <div className="range-container">
                        <input
                            type="range"
                            id="minPrice"
                            name="minPrice"
                            value={formData.minPrice}
                            onChange={handleChange}
                            min="0"
                            max="1000000"
                            step="10000"
                        />
                        <span className="range-value">${formData.minPrice}</span>
                    </div>
                    <div className="range-container">
                        <input
                            type="range"
                            id="maxPrice"
                            name="maxPrice"
                            value={formData.maxPrice}
                            onChange={handleChange}
                            min="0"
                            max="1000000"
                            step="10000"
                        />
                        <span className="range-value">${formData.maxPrice}</span>
                    </div>
                </div>
            </div>

            <button type="submit" className="submit-button">
                Search Properties
            </button>
        </form>
    );
};

export default InsightsForm; 