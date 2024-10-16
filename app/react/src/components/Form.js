import React, { useState, useEffect } from 'react';
import Dropdown from './Dropdown';
import TextInput from './TextInput';
import Header from './Header';

const Form = ({onSubmit,loading}) => {
    // Form state management
   const [formData, setFormData] = useState({
        entries: 0,
        update: '',
        operation: '',
        type: '',
        state: '',
        city: '',
        neighborhood: '',
        dorm: '',
        toilet: '',
        garage:'',
        min_size: '',
        max_size: '',
        min_price: '',
        max_price: '',
        operations: [],
        types: [],
        states: [],
        cities: [],
        neighborhoods: [],
        dorms: [],
        toilets: [],
        garages:[]
   });

    // Fetch data from the backend on component mount
    useEffect(() => {
        fetch("http://127.0.0.1:5000/initial")
            .then(response => response.json())
            .then(data => {
                setFormData(prev => ({
                    ...prev,
                    ...data,
                    operation: data.operations[0] || '',
                    type: data.types[0] || '',
                    state: data.states[0] || '',
                    city: data.cities[0] || '',
                    neighborhood: data.neighborhoods[0] || '',
                    dorm: data.dorms[0] || '',
                    toilet: data.toilets[0] || '',
                    garage: data.garages[0] || ''
                }));
            })
            .catch(err => {
                console.error("Error fetching form data:", err);
            });

    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
         setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(formData);
    };

    return (
        <div className="form-container">
            <Header entries={formData.entries} update={formData.update} />

            <form className="custom-form" onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="operation">Operation</label>
                    <Dropdown
                        label=""
                        name="operation"
                        value={formData.operation}
                        options={formData.operations}
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="type">Type</label>
                    <Dropdown
                        label=""
                        name="type"
                        value={formData.type}
                        options={formData.types}
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="state">State</label>
                    <Dropdown
                        label=""
                        name="state"
                        value={formData.state}
                        options={formData.states}
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="city">City</label>
                    <Dropdown
                        label=""
                        name="city"
                        value={formData.city}
                        options={formData.cities}
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="neighborhood">Neighborhood</label>
                    <Dropdown
                        label=""
                        name="neighborhood"
                        value={formData.neighborhood}
                        options={formData.neighborhoods}
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="dorm">Number of Dorms</label>
                    <Dropdown
                        label=""
                        name="dorm"
                        value={formData.dorm}
                        options={formData.dorms}
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="toilet">Number of Toilets</label>
                    <Dropdown
                        label=""
                        name="toilet"
                        value={formData.toilet}
                        options={formData.toilets}
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="garage">Number of Garages</label>
                    <Dropdown
                        label=""
                        name="garage"
                        value={formData.garage}
                        options={formData.garages}
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="min_size">Mininum Size</label>
                    <TextInput
                        label=""
                        name="min_size"
                        value={formData.min_size}
                        type="number"
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="max_size">Maximum Size</label>
                    <TextInput
                        label=""
                        name="max_size"
                        value={formData.max_size}
                        type="number"
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="min_price">Mininum Price</label>
                    <TextInput
                        label=""
                        name="min_price"
                        value={formData.min_price}
                        type="number"
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="max_price">Maximum Price</label>
                    <TextInput
                        label=""
                        name="max_price"
                        value={formData.max_price}
                        type="number"
                        onChange={handleChange}
                    />
                </div>

                <div className="form-buttons">
                    <button className="submit-button" type="submit" disabled={loading}>
                        {loading ? 'Processing...' : 'Submit'}
                    </button>
                </div>
            </form>
        </div>

    );
};

export default Form;
