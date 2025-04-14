const SelectionField = ({ id, title, options, selectedValue, onChange, required = false }) => {

    return (
        <div className={`form-group ${required ? 'required' : ''} ${options.length === 0 ? 'disabled' : ''}`}>
            <label className={required ? 'required' : ''}>{title}</label>
            <select
                id={id}
                name={id}
                value={selectedValue}
                onChange={onChange}
                disabled={options.length === 0}
            >
                {options.map((option) => (
                    <option key={option.value} value={option.value}>{option.label}</option>
                ))}
            </select>
        </div>
    );
};

export default SelectionField;