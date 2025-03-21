import React, {useState} from 'react';
import Figure from './Figure';
import SummaryModel from './SummaryModel';
import FormPredictor from './FormPredictor';

const ModelReport = ({ data }) => {
    const { features_analysis, model, mse, mae, r2, summary_model, predictions_plot } = data;
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
        console.log(inputData);
    };

    return (
        <div className="report">
            {/* Features Importance */}
            {/*<div className="report-section">
                <h2>Features Importance</h2>
                <Figure figure={features_analysis} width={98} alt="Features Importance" />
            </div>

            {/* Model Summary */}
            {/*<div className="report-section" >
                <SummaryModel model={model} mse={mse} mae={mae} r2={r2} summary={summary_model} />
                <Figure figure={predictions_plot} alt="Predicted vs Actuals Plot" width={98} />
            </div>

            {/* Price Predictor */}
             <div className="report-section price-predictor-section">
                <h2 className="report-title">Price Predictor</h2>
                <FormPredictor onPredict={handlePredict} />
                {predictions !== null && (
                    <div className="main-summary">
                        <h2 className="report-title">Results</h2>
                        <div className="summary-details">
                            <p><strong>Predicted Price:</strong> {predictions.price.toFixed(2)}</p>
                            <p><strong>Predicted Additional Costs:</strong> {predictions.additional_costs.toFixed(2)}</p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ModelReport;
