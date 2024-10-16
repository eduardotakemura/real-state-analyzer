import React from 'react';
import Figure from './Figure';  // Assume the Figure component is used to render plots

const SummaryModel = ({ model, mse, mae, r2, summary }) => {
    return (
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <div>
                <h4>Predictor Model Summary</h4>
                <p><strong>Model:</strong> {model}</p>
                <p><strong>MSE:</strong> {mse.toFixed(2)}</p>
                <p><strong>MAE:</strong> {mae.toFixed(2)}</p>
                <p><strong>R2 Score:</strong> {r2.toFixed(2)}</p>
            </div>
            <div>
                <h4>Summary Statistics</h4>
                <table>
                    <thead>
                        <tr>
                            <th>Average Actual Price</th>
                            <th>Average Predicted Price</th>
                            <th>Average Absolute Error</th>
                            <th>Average Percentage Error (%)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{summary[0]['Average Actual Price'].toFixed(2)}</td>
                            <td>{summary[0]['Average Predicted Price'].toFixed(2)}</td>
                            <td>{(summary[0]['Average Absolute Error']* 100).toFixed(2)}</td>
                            <td>{(summary[0]['Average Percentage Error (%)']* 100).toFixed(2)}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default SummaryModel;
