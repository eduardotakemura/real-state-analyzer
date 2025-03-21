import React from 'react';

const TextInput = ({ label, name, value, onChange, type = "text" }) => {
    return (
        <div className="form-group">
            <label>{label}</label>
            <input
                type={type}
                name={name}
                value={value}
                onChange={onChange}
            />
        </div>
    );
};

export default TextInput;
