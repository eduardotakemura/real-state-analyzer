import React from 'react';
import './Header.css';

const Header = () => {
    return (
        <header className="header">
            <div className="header-content">
                <h1>Real Estate Analyzer</h1>
                <nav className="nav-links">
                    <a href="https://github.com/eduardotakemura/real-state-analyzer">Repository</a>
                </nav>
            </div>
        </header>
    );
};

export default Header; 