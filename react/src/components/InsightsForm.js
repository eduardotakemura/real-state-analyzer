import React, { useState, useEffect } from 'react';
import SelectionField from './SelectionField.js';
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
        maxSize: '0',
        minPrice: '0',
        maxPrice: '0'
    });

    const [options, setOptions] = useState({
        count: 0,
        operations: [],
        types: [],
        cities: [],
        neighborhoods: [],
        maxSize: 0,
        minSize: 0,
        maxPrice: 0,
        minPrice: 0
    });

    useEffect(() => {
        fetch('http://localhost:8000/properties/initial-options')
            .then(response => response.json())
            .then(data =>
                setOptions({
                    count: data.count,
                    operations: data.operations,
                    types: [],
                    cities: [],
                    neighborhoods: [],
                    minSize: 0,
                    maxSize: 0,
                    minPrice: 0,
                    maxPrice: 0
                })
            );
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleOperationChange = (e) => {
        // Update operation in form data
        setFormData(prev => ({
            ...prev,
            operation: e.target.value
        }));

        // Fetch options for operation
        fetch(`http://localhost:8000/properties/options/${e.target.value}`)
            .then(response => response.json())
            .then(data => setOptions({
                count: data.count,
                operations: options.operations,
                types: data.types,
                cities: data.cities,
                neighborhoods: data.neighborhoods,
                minSize: data.minSize,
                maxSize: data.maxSize,
                minPrice: data.minPrice,
            }));
        console.log(options);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // TODO: Implement API call to backend
        console.log('Form submitted:', formData);
    };

    return (
        <form onSubmit={handleSubmit} className="insights-form">
            <p> {options.count} </p>
            {/* Row 1: Operation */}
            <SelectionField
                id="operation"
                title="Select Desired Operation (Selling/Renting)"
                options={options.operations ?
                    [{ value: '', label: 'Select Operation' }, ...options.operations.map(operation => ({ value: operation, label: operation.charAt(0).toUpperCase() + operation.slice(1) }))] : []}
                selectedValue={formData.operation}
                onChange={handleOperationChange}
                required={true}
            />

            {/* Row 2: Type, City and Neighborhood */}
            <div className="form-row">
                <SelectionField
                    id="type"
                    title="Select Property Type"
                    options={options.types ? options.types.map(type => ({ value: type, label: type })) : []}
                    selectedValue={formData.type}
                    onChange={handleChange}
                />

                <SelectionField
                    id="city"
                    title="Select City"
                    options={options.cities ? options.cities.map(city => ({ value: city, label: city })) : []}
                    selectedValue={formData.city}
                    onChange={handleChange}
                />

                <SelectionField
                    id="neighborhood"
                    title="Select Neighborhood"
                    options={options.neighborhoods ? options.neighborhoods.map(neighborhood => ({ value: neighborhood, label: neighborhood })) : []}
                    selectedValue={formData.neighborhood}
                    onChange={handleChange}
                />
            </div>

            {/* Row 3: Bedrooms, Bathrooms, Garage */}
            <div className="form-row">
                <SelectionField
                    id="dorms"
                    title="Number of Bedrooms"
                    options={[{ value: 0, label: 'Any' }, { value: 1, label: '1+' }, { value: 2, label: '2+' }, { value: 3, label: '3+' }]}
                    selectedValue={formData.dorms}
                    onChange={handleChange}
                />

                <SelectionField
                    id="toilets"
                    title="Number of Bathrooms"
                    options={[{ value: 0, label: 'Any' }, { value: 1, label: '1+' }, { value: 2, label: '2+' }, { value: 3, label: '3+' }]}
                    selectedValue={formData.toilets}
                    onChange={handleChange}
                />

                <SelectionField
                    id="garage"
                    title="Garage Spaces"
                    options={[{ value: 0, label: 'Any' }, { value: 1, label: '1+' }, { value: 2, label: '2+' }, { value: 3, label: '3+' }]}
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
                            id="minSize"
                            name="minSize"
                            value={formData.minSize}
                            onChange={handleChange}
                            min={options.minSize}
                            max={options.maxSize}
                            step="20"
                        />
                        <span className="range-value">{formData.minSize} m²</span>
                    </div>
                    <div className="range-container">
                        <input
                            type="range"
                            id="maxSize"
                            name="maxSize"
                            value={formData.maxSize}
                            onChange={handleChange}
                            min={options.minSize}
                            max={options.maxSize}
                            step="20"
                        />
                        <span className="range-value">{formData.maxSize} m²</span>
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
                            min={options.minPrice}
                            max={options.maxPrice}
                            step="10000"
                        />
                        <span className="range-value">R${formData.minPrice}</span>
                    </div>
                    <div className="range-container">
                        <input
                            type="range"
                            id="maxPrice"
                            name="maxPrice"
                            value={formData.maxPrice}
                            onChange={handleChange}
                            min={options.minPrice}
                            max={options.maxPrice}
                            step="10000"
                        />
                        <span className="range-value">R${formData.maxPrice}</span>
                    </div>
                </div>
            </div>

            <button type="submit" className={`submit-button ${formData.operation == '' ? 'disabled' : ''}`}>
                Search Properties
            </button>
        </form>
    );
};

export default InsightsForm; 