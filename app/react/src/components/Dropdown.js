import React from 'react';

const Dropdown = ({ label, options, name, value, onChange }) => {
    return (
        <div className="form-group">
            <label>{label}</label>
            <select name={name} value={value} onChange={onChange}>
                {options.map((option, index) => (
                    <option key={index} value={option}>
                        {option}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default Dropdown;
