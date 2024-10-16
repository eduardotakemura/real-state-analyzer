import React, {useState} from 'react';
import SummaryModel from './SummaryModel';
import FormPredictor from './FormPredictor';

const ModelReport = () => {
    const [predictions, setPredictions] = useState(null);

    const handlePredict = async (inputData) => {
        // Fetch the predicted price from the backend
        const response = await fetch('http://127.0.0.1:5000/get_prediction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(inputData),
        });
        const data = await response.json();
        setPredictions(data);
    };

    return (
        <div className="report">
            {/* Price Predictor */}
             <div className="report-section price-predictor-section">
                <h2 className="report-title">Price Predictor</h2>
                <FormPredictor onPredict={handlePredict} />
                {predictions !== null && (
                    <div className="main-summary">
                        <h2 className="report-title">Results</h2>
                        <div className="summary-details">
                            <p><strong>Predicted Price:</strong> {predictions.prediction.toFixed(2)}</p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ModelReport;
