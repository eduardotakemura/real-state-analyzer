import './App.css';
import React, { useState, useRef, useEffect } from 'react';
import Form from './components/Form';
import AnaliseReport from './components/AnaliseReport';
import ModelReport from './components/ModelReport';

function App() {
    const [analise, setAnalise] = useState(null);
    const [loading, setLoading] = useState(false);
    const reportRef = useRef(null);

    useEffect(() => {
        if (analise) {
            // Ensure the content is fully rendered before scrolling
            setTimeout(() => {
                if (reportRef.current) {
                    reportRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }, 100); // Adjust timeout if needed
        }
    }, [analise]);

    const handleFormSubmit = (formData) => {
        setLoading(false);

        fetch("http://127.0.0.1:5000/get_entries_count", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        })
        .then(response => response.json())
        .then(data => {
            const entryCount = data.entries_count;
            const proceed = window.confirm(`Number of entries found: ${entryCount}. Do you want to proceed?`);

            if (proceed) {
                setLoading(true);
                setAnalise(null);

                // Analise Fetch
                fetch("http://127.0.0.1:5000/get_analysis", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData),
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    setAnalise(data);
                    setLoading(false);

                })
                .catch((error) => {
                    console.error("Error:", error);
                    setLoading(false);
                });
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    }

  return (
    <div className="App">
        <Form onSubmit={handleFormSubmit} loading={loading}/>
        <div ref={reportRef}>
            {analise && <AnaliseReport data={analise} />}
            {analise && <ModelReport />}
        </div>
    </div>
  );
}

export default App;
