import React, { useState } from 'react';
import TextInput from './TextInput';

const FormPredictor = ({ onPredict }) => {
    const [inputData, setInputData] = useState({
        size: '',
        dorms: '',
        toilets: '',
        garage: '',
        type: '',
        location: '',
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setInputData({
            ...inputData,
            [name]: value,
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onPredict(inputData); // Trigger prediction function passed as a prop
    };

    return (
        <form className="form-predictor" onSubmit={handleSubmit}>
            <TextInput
                label="Size (m²)"
                name="size"
                value={inputData.size}
                onChange={handleChange}
                type="number"
            />
            <TextInput
                label="Dorms"
                name="dorms"
                value={inputData.dorms}
                onChange={handleChange}
                type="number"
            />
            <TextInput
                label="Toilets"
                name="toilets"
                value={inputData.toilets}
                onChange={handleChange}
                type="number"
            />
            <TextInput
                label="Garage"
                name="garage"
                value={inputData.garage}
                onChange={handleChange}
                type="number"
            />
            <TextInput
                label="Type (1 for Apartment, 0 for House)"
                name="type"
                value={inputData.type}
                onChange={handleChange}
                type="number"
            />
            <TextInput
                label="Location"
                name="location"
                value={inputData.location}
                onChange={handleChange}
                type="number"
            />
            <button className="submit-button" type="submit">Predict Price</button>
        </form>
    );
};

export default FormPredictor;
