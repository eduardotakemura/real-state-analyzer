import React from 'react';

const Header = ({ entries, update }) => {
    return (
        <div className='header'>
            <h1 className="header-title">Real Estate Analyzer</h1>
            <p className="header-description">Select the desired filters and press 'Submit' to get a custom report for this dataset.</p>
            <div className='header-info'>
                <p className='header-fields'>Information About: {entries} real states</p>
                <p className='header-fields'>Last Update:{update}</p>
            </div>
        </div>
    );
};

export default Header;
